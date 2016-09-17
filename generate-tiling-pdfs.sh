#### Usage: generate-tiling-pdfs.sh <TilingByName> <LowerN> <UpperN>
#!/bin/bash 

CONVERT=convert
PDFJAM=pdfjam-slides3up
OUTPUT=./output
TILING=$1
SAGE=sage
FILES=""

#### Generate the histogram images: 
for N in `seq $2 $3`; 
do 
     $SAGE -python tiling_pc_plots.py -t $TILING -s -n $N
     $SAGE -python tiling_pc_plots.py -t $TILING -s -n $N -q
     $SAGE -python tiling_pc_plots.py -t $TILING -s -n $N -a
     $SAGE -python tiling_pc_plots.py -t $TILING -s -n $N -d
     $SAGE -python tiling_pc_plots.py -t $TILING -s -n $N -l
     $SAGE -python tiling_pc_plots.py -t $TILING -s -n $N -g
done

echo "Regenerating PDFs for tiling \"$TILING\" ... "

#### Create the pdfs from the histogram and tiling image output:
cd $OUTPUT 
for image in $( ls $TILING-*.png ); do 
     $CONVERT $image $image.pdf
done 

echo "Calling PDFJAM for tiling \"$TILING\" ... "

#### Compile the summary pdfs for this tiling: 
SUFFIX=("pc-edist" "pc-edistsq" "angles" "anglegaps" "slopes" "slopegaps")
NUMBINS=("000150" "000500" "010000")
for suffix in "${SUFFIX[@]}";
do 
     FILES=""
     for numbins in "${NUMBINS[@]}"; 
     do 
          for pdf in $(ls $TILING-NUMBINS.$numbins*$suffix.png.pdf); 
          do 
               FILES="$FILES $pdf"
          done 
     done
     $PDFJAM --outfile ../pdfs/$TILING-$suffix.pdf $FILES 
done 

suffix="tiling"
for pdf in $(ls $TILING-*$suffix.png.pdf); 
do 
     FILES="$FILES $pdf"
done 
$PDFJAM --outfile ../pdfs/$TILING-$suffix.pdf $FILES 

rm *png.pdf

echo -e "DONE WITH TILING $TILING\n\n"



