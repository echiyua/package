#!/bin/bash



function readDir(){
	targetDir=`ls DU_$1`
	echo "targetDir:$targetDir"
  echo "**************"
	cd ~ && mkdir DU_$1_decode
	for filename in $targetDir
	do
		if [ -f ~/DU_$1/$filename ]
		then
			if [[ ${filename:0-4} == '.log' ]]
			then
        echo "~/DU_$1/$filename"
        #ll ~/DU_$1/$filename 
        #cp ~/DU_$1/$filename ~/DU_$1_decode/decode_$filename
				#cat ~/DU_$1/$filename | ltng-decoder -s -t ~/xml > ~/DU_$1_deocde/decode_$filename
        ltng-decoder -f ~/DU_$1/$filename > ~/DU_$1_decode/decode_$filename
			fi
		fi
	done
}

readDir $1
