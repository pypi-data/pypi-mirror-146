Experiment="7603"
sedinput=$(sed 's/\//\\\//g' <<< "$input")
sedoutput=$(sed 's/\//\\\//g' <<< "$output")
sedlib=$(sed 's/\//\\\//g' <<< "$lib")
rep="tmp"

printf "Running PanChIP filter...\n"

lib2sum() {
sort -u -k1,1 -k2,2n -k3,3n -k4,4n $input/$1.bed | awk 'function abs(v) {return v < 0 ? -v : v} BEGIN{var=0} {var=var+$5*abs($3-$2)} END{print var}' > $input/$1.sum
}
rep2sum() {
sort -u -k1,1 -k2,2n -k3,3n -k4,4n $lib/$1.bed | awk 'function abs(v) {return v < 0 ? -v : v} BEGIN{var=0} {var=var+$5*abs($3-$2)} END{print var}' > $lib/$rep/$1.sum
}
lib2wc() {
wc -l $input/$1.bed | awk '{print $1}' > $input/$1.wc
}

mkdir -p $lib/$rep
for i in $inputfiles
do
lib2sum "$i"
lib2wc "$i"
done
echo $inputfiles | sed -e 's/ /.sum '$sedinput'\//g' -e 's/^/'$sedinput'\//' -e 's/$/.sum/' | xargs cat > $input/SUM.count
echo $inputfiles | sed -e 's/ /.sum '$sedinput'\//g' -e 's/^/'$sedinput'\//' -e 's/$/.sum/' | xargs rm
echo $inputfiles | sed -e 's/ /.wc '$sedinput'\//g' -e 's/^/'$sedinput'\//' -e 's/$/.wc/' | xargs cat > $input/WC.count
echo $inputfiles | sed -e 's/ /.wc '$sedinput'\//g' -e 's/^/'$sedinput'\//' -e 's/$/.wc/' | xargs rm
paste $input/SUM.count $input/WC.count | awk '{print $1/$2}' > $input/SUMdivbyWC.count
for cnt in $(seq 1 1 $Experiment)
do
  if [ $(jobs -r | wc -l) -ge $threads ]; then
    wait $(jobs -r -p | head -1)
  fi
  (rep2sum "$cnt") &
done
printf ""
wait
seq $Experiment | sed 's:.*:'$sedlib'\/'$rep'\/&.sum:' | xargs cat > $lib/$rep/SUM.count
seq $Experiment | sed 's:.*:'$sedlib'\/'$rep'\/&.sum:' | xargs rm

subtask1() {
bedtools intersect -a $input/$1.bed -b $lib/$2.bed | sort -u -k1,1 -k2,2n -k3,3n -k4,4n | awk 'function abs(v) {return v < 0 ? -v : v} BEGIN{var=0} {var=var+$5*abs($3-$2)} END{print var}' > $output/$3/$1/intersect.$2.count
bedtools intersect -a $lib/$2.bed -b $input/$1.bed | sort -u -k1,1 -k2,2n -k3,3n -k4,4n | awk 'function abs(v) {return v < 0 ? -v : v} BEGIN{var=0} {var=var+$5*abs($3-$2)} END{print var}' > $output/$3/$1/intersect2.$2.count
}
catfunc() {
seq $Experiment | sed 's:.*:'$2'.&.count:' | xargs cat > $1.dist
}
subtask2() {
catfunc "$output/$2/$1/intersect" "$sedoutput\/$2\/$1\/intersect"
catfunc "$output/$2/$1/intersect2" "$sedoutput\/$2\/$1\/intersect2"
rm $output/$2/$1/intersect.*.count
rm $output/$2/$1/intersect2.*.count
sort -u -k1,1 -k2,2n -k3,3n -k4,4n $input/$2/$1.bed | awk 'function abs(v) {return v < 0 ? -v : v} BEGIN{var=0} {var=var+$5*abs($3-$2)} END{print var}' > $output/$2/$1/$1.dist
awk '{for(i=1;i<='$Experiment';i++) {print}}' $output/$2/$1/$1.dist > $output/$2/$1/$1.tmp
paste $output/$2/$1/intersect.dist $output/$2/$1/intersect2.dist $lib/$2/SUM.count $output/$2/$1/$1.tmp | awk '{print sqrt($1*$2/$3/$4)}' > $output/$2/$1/intersect.normalized.dist
rm $output/$2/$1/$1.tmp $output/$2/$1/intersect.dist $output/$2/$1/intersect2.dist
}
task1() {
mkdir -p $output/$2/$1
for factor in $(seq 1 1 $Experiment)
do
subtask1 "$1" "$factor" "$2"
done
subtask2 "$1" "$2"
}
task2() {
echo $rep | sed 's:.*:'$sedoutput'\/&\/'$1'\/intersect.normalized.dist:' | xargs paste -d ' ' | numsum -r | awk '{print $1/'$rep'}' > $output/$1.txt
}

mkdir -p $output
mkdir -p $output/$rep
for file in $inputfiles
do
  if [ $(jobs -r | wc -l) -ge $threads ]; then
    wait $(jobs -r -p | head -1)
  fi
  (echo Begin processing $file; task1 "$file" "$rep") &
done
wait
printf "Processing output files...\n"
for file in $inputfiles
do
  if [ $(jobs -r | wc -l) -ge $threads ]; then
    wait $(jobs -r -p | head -1)
  fi
  (task2 "$file") &
done
wait
echo $inputfiles | sed -e 's/ /.txt '$sedoutput'\//g' -e 's/^/'$sedlib'\/Experiment.txt '$sedoutput'\//' -e 's/$/.txt/' | xargs paste | awk 'BEGIN{print "'$(sed -e 's/ /\\t/g' -e 's/^/TR\\t/' <<< $inputfiles)'"} {print}' > $output/primary.output.tsv
for file in $inputfiles
do
rm $output/$file.txt
done
rm -r $lib/$rep
rm -r $output/$rep
mkdir -p $output/input.stat
for file in SUM SUMdivbyWC WC
do
mv $input/$file.count $output/input.stat/$file.count
done
printf "Completed PanChIP filter!\n"
