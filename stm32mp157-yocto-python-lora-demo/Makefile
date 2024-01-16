docker:
	docker build -t yocto-builder . && \
	docker run --rm -it \
	--security-opt seccomp=unconfined \
	-v  $${PWD}:$${PWD}:Z \
	-v ~/.gitconfig:/etc/gitconfig:Z \
	yocto-builder \
	--workdir=$${PWD}


build:
	docker run --rm -it \
	--security-opt seccomp=unconfined \
	-v  $${PWD}:$${PWD}:Z \
	-v ~/.gitconfig:/etc/gitconfig:Z \
	yocto-builder \
	--workdir=$${PWD} \
	/bin/bash -c 'source ./layers/openembedded-core/oe-init-build-env ./build-openstlinuxweston-stm32mp1/ && bitbake st-image-weston && exit'

env:
	docker run --rm -it \
	--security-opt seccomp=unconfined \
	-v  $${PWD}:$${PWD}:Z \
	-v ~/.gitconfig:/etc/gitconfig:Z \
	yocto-builder \
	--workdir=$${PWD} \
	/bin/bash -c 'source ./layers/openembedded-core/oe-init-build-env build-openstlinuxweston-stm32mp1/ && bash'

flash:
	cd ./build-openstlinuxweston-stm32mp1/tmp-glibc/deploy/images/stm32mp1/ && STM32_Programmer_CLI -c port=usb1 -w flashlayout_st-image-weston/trusted/FlashLayout_sdcard_stm32mp157c-dk2-trusted.tsv && cd -
