paper_dir=temp/paper
mkdir -p "$paper_dir"
sbatch_dir=temp/paper/sbatch
mkdir -p "$sbatch_dir"

wall_time="23:59:00"
memory="60GB"

# Rough runs using BPOSD decoder on toric code
for repeat in $(seq 1 6); do
    name=unrot_bposd_xzzx_zbias_$repeat
    rm -rf $paper_dir/$name/inputs
    rm -rf $paper_dir/$name/logs
    panqec generate-input -i "$paper_dir/$name/inputs" \
        --lattice kitaev --boundary toric --deformation xzzx --ratio equal  \
        --sizes "9,13,17,21" --decoder BeliefPropagationOSDDecoder --bias Z \
        --eta "30,100" --prob "0:0.5:0.02"
    panqec cc-sbatch --data_dir "$paper_dir/$name" --n_array 50 --memory $memory \
        --wall_time "$wall_time" --trials 1667 --split 1 $sbatch_dir/$name.sbatch

    name=unrot_bposd_undef_zbias_$repeat
    rm -rf $paper_dir/$name/inputs
    rm -rf $paper_dir/$name/logs
    panqec generate-input -i "$paper_dir/$name/inputs" \
        --lattice kitaev --boundary toric --deformation none --ratio equal \
        --sizes "9,13,17,21" --decoder BeliefPropagationOSDDecoder --bias Z \
        --eta "30,100" --prob "0:0.5:0.02"
    panqec cc-sbatch --data_dir "$paper_dir/$name" --n_array 50 --memory $memory \
        --wall_time "$wall_time" --trials 1667 --split 1 $sbatch_dir/$name.sbatch
done
