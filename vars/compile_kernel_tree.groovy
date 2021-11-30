def call(version, log) {
	sh """
		pushd linux
		git checkout "${version}"
		make defconfig
		/usr/bin/time -o "../${log}" -p make -j 2
		popd
	"""
}
