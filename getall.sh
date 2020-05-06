#!/bin/bash

scripts=($(ls gomiget_aichi_*.py))

for script in ${scripts[@]}; do
	to=$(echo ${script} | sed -e "s/gomiget_\([a-z_]\+\)\.py/gomidata_\1.json/")
	echo "${script} > ${to}"
	./${script} > ${to}
done

echo "終わりました。"
