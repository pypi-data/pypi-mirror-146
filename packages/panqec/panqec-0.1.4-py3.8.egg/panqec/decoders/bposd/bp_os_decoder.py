from typing import Dict
import numpy as np
from qecsim.model import Decoder, StabilizerCode, ErrorModel
from typing import Tuple
from ldpc import bposd_decoder


class BeliefPropagationOSDDecoder(Decoder):
    label = 'BP-OSD decoder'

    def __init__(self, error_model: ErrorModel,
                 probability: float,
                 max_bp_iter: int = 10,
                 channel_update: bool = False):
        super().__init__()
        self._error_model = error_model
        self._probability = probability
        self._max_bp_iter = max_bp_iter
        self._channel_update = channel_update

        self._x_decoder: Dict = dict()
        self._z_decoder: Dict = dict()
        self._decoder: Dict = dict()

    def get_probabilities(
        self, code: StabilizerCode
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:

        pi, px, py, pz = self._error_model.probability_distribution(
            code, self._probability
        )

        return pi, px, py, pz

    def update_probabilities(self, correction: np.ndarray,
                             px: np.ndarray, py: np.ndarray, pz: np.ndarray,
                             direction: str = "x->z") -> np.ndarray:
        """Update X probabilities once a Z correction has been applied"""

        n_qubits = correction.shape[0]

        new_probs = np.zeros(n_qubits)

        if direction == "z->x":
            for i in range(n_qubits):
                if correction[i] == 1:
                    if pz[i] + py[i] != 0:
                        new_probs[i] = py[i] / (pz[i] + py[i])
                else:
                    new_probs[i] = px[i] / (1 - pz[i] - py[i])

        elif direction == "x->z":
            for i in range(n_qubits):
                if correction[i] == 1:
                    if px[i] + py[i] != 0:
                        new_probs[i] = py[i] / (px[i] + py[i])
                else:
                    new_probs[i] = pz[i] / (1 - px[i] - py[i])

        else:
            raise ValueError(
                f"Unrecognized direction {direction} when "
                "updating probabilities"
            )

        return new_probs

    def decode(self, code: StabilizerCode, syndrome: np.ndarray) -> np.ndarray:
        """Get X and Z corrections given code and measured syndrome."""

        is_css = code.is_css

        n_qubits = code.n
        syndrome = np.array(syndrome, dtype=int)

        if is_css:
            syndrome_z = code.extract_z_syndrome(syndrome)
            syndrome_x = code.extract_x_syndrome(syndrome)

        pi, px, py, pz = self.get_probabilities(code)

        probabilities_x = px + py
        probabilities_z = pz + py

        probabilities = np.hstack([probabilities_z, probabilities_x])

        # Load saved decoders
        if code.label in self._x_decoder.keys():
            x_decoder = self._x_decoder[code.label]
            z_decoder = self._z_decoder[code.label]
        elif code.label in self._decoder.keys():
            decoder = self._decoder[code.label]

        # Initialize new decoders otherwise
        else:
            if is_css:
                z_decoder = bposd_decoder(
                    code.Hx,
                    error_rate=0.05,  # ignore this due to the next parameter
                    channel_probs=probabilities_z,
                    max_iter=self._max_bp_iter,
                    bp_method="msl",
                    ms_scaling_factor=0,
                    osd_method="osd_cs",  # Choose from: "osd_e", "osd_cs", "osd0"
                    osd_order=6
                )

                x_decoder = bposd_decoder(
                    code.Hz,
                    error_rate=0.05,  # ignore this due to the next parameter
                    channel_probs=probabilities_x,
                    max_iter=self._max_bp_iter,
                    bp_method="msl",
                    ms_scaling_factor=0,
                    osd_method="osd_cs",  # Choose from: "osd_e", "osd_cs", "osd0"
                    osd_order=6
                )
                self._x_decoder[code.label] = x_decoder
                self._z_decoder[code.label] = z_decoder
            else:
                decoder = bposd_decoder(
                    code.stabilizer_matrix,
                    error_rate=0.05,  # ignore this due to the next parameter,
                    channel_probs=probabilities,
                    max_iter=self._max_bp_iter,
                    bp_method="msl",
                    ms_scaling_factor=0,
                    osd_method="osd_cs",  # Choose from: "osd_e", "osd_cs", "osd0"
                    osd_order=6
                )
                self._decoder[code.label] = decoder

        if is_css:
            # Update probabilities (in case the distribution is new at each iteration)
            x_decoder.update_channel_probs(probabilities_x)
            z_decoder.update_channel_probs(probabilities_z)

            # Decode Z errors
            z_decoder.decode(syndrome_x)
            z_correction = z_decoder.osdw_decoding

            # Bayes update of the probability
            if self._channel_update:
                new_x_probs = self.update_probabilities(
                    z_correction, px, py, pz, direction="z->x"
                )
                x_decoder.update_channel_probs(new_x_probs)

            # Decode X errors
            x_decoder.decode(syndrome_z)
            x_correction = x_decoder.osdw_decoding

            correction = np.concatenate([x_correction, z_correction])
        else:
            # Update probabilities (in case the distribution is new at each iteration)
            decoder.update_channel_probs(probabilities)

            # Decode all errors
            decoder.decode(syndrome)
            correction = decoder.osdw_decoding
            correction = np.concatenate([correction[n_qubits:], correction[:n_qubits]])

        return correction


def test_decoder():
    from panqec.codes import Toric3DCode
    from panqec.bpauli import bcommute, get_effective_error
    from panqec.error_models import DeformedRandomErrorModel
    import time
    rng = np.random.default_rng()

    L = 20
    code = Toric3DCode(L, L, L)

    probability = 0.1
    r_x, r_y, r_z = [0.1, 0.1, 0.8]
    error_model = DeformedRandomErrorModel(r_x, r_y, r_z, p_xz=0.5, p_yz=0.5)

    decoder = BeliefPropagationOSDDecoder(
        error_model, probability
    )

    # Start timer
    start = time.time()

    n_iter = 5
    for i in range(n_iter):
        print(f"\nRun {code.label} {i}...")
        print("Generate errors")
        error = error_model.generate(code, probability=probability, rng=rng)
        print("Calculate syndrome")
        syndrome = bcommute(code.stabilizer_matrix, error)
        print("Decode")
        correction = decoder.decode(code, syndrome)
        print("Get total error")
        total_error = (correction + error) % 2
        print("Get effective error")
        effective_error = get_effective_error(
            total_error, code.logicals_x, code.logicals_z
        )
        print("Check codespace")
        codespace = bool(np.all(bcommute(code.stabilizer_matrix, total_error) == 0))
        success = bool(np.all(effective_error == 0)) and codespace
        print(success)

    print("Average time per iteration", (time.time() - start) / n_iter)


if __name__ == '__main__':
    test_decoder()
