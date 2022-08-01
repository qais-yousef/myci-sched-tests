def call(priority, duration, interval) {
	switch (env.MYCI_NODE_TYPE) {
	case "android":
		if (env.IPADDRESS && env.PORT) {
			sh """
				file="/data/cyclictest.json"
				adb -s ${IPADDRESS}:${PORT} shell "cyclictest -t -p ${priority} -D ${duration} -i ${interval} --laptop --json=\$file"
				adb -s ${IPADDRESS}:${PORT} pull \$file
				adb -s ${IPADDRESS}:${PORT} shell "rm \$file"
			"""
		} else {
			error "Missing IPADDRESS and/or PORT info"
		}
		break
	case "linux":
		sh """
			cyclictest -t -p ${priority} -D ${duration} -i ${interval} --laptop --json=cyclictest.json
		"""
		break
	default:
		break
	}
}
