def call() {
	sh """
		if [ -d linux ]; then
			pushd linux
			make mrproper
			git clean -f
			popd
		fi
	"""
}
