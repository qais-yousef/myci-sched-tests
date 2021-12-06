def call(version, log, uclamp_min, uclamp_max, num_parallel_jobs) {
	sh """
		pushd linux
		git checkout "${version}"
		make defconfig
		uclampset -m ${uclamp_min} -M ${uclamp_max} \
			/usr/bin/time -o "../${log}" -p make -j ${num_parallel_jobs}
		popd
	"""
}
