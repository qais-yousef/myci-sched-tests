def call(priority, duration, interval, num_threads) {
	switch (env.MYCI_NODE_TYPE) {
	case "android":
		if (env.IPADDRESS && env.PORT) {
			sh """
				file="/data/cyclictest.json"
				adb -s ${IPADDRESS}:${PORT} shell "cyclictest -t ${num_threads} -p ${priority} -D ${duration} -i ${interval} --json=\$file"
				adb -s ${IPADDRESS}:${PORT} pull \$file
				adb -s ${IPADDRESS}:${PORT} shell "rm \$file"
			"""
		} else {
			error "Missing IPADDRESS and/or PORT info"
		}
		break
	case "linux":
		sh """
			cyclictest -t ${num_threads} -p ${priority} -D ${duration} -i ${interval} --json=cyclictest.json
		"""
		break
	default:
		break
	}
}
