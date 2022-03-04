def call() {
	switch (env.MYCI_NODE_TYPE) {
	case "android":
		if (env.IPADDRESS && env.PORT) {
			sh """
				adb -s ${IPADDRESS}:${PORT} shell -x 'cmd package compile -m speed-profile -f -a'
			"""
		} else {
			error "Missing IPADDRESS and/or PORT info"
		}
		break
	case "linux":
	default:
		error "Only supported on Android"
		break
	}
}
