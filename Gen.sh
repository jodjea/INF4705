#!/bin/bash
if [ -f ex_* ]; then
    rm ex_*
fi

#if [ -f testset* ]; then
 #   rm -r testset*
#fi
rm -r $(ls | grep "testset*")

for N in {6..10}; do
	for I in {1..5}; do
		./Gen $N "ex_"$N"."$I
	done
done

for i in {6..10}; do
    mkdir testset${i}

    mv $(ls | grep "_${i}.[0-9]") ./testset${i}
done
