def call(iterations, delay) {
	switch (env.MYCI_NODE_TYPE) {
	case "android":
		if (env.IPADDRESS && env.PORT) {
			sh """
				for i in \$(seq ${iterations})
				do
					echo "Iteration [\$i]"
					echo "Waiting ${delay}s before starting..."
					sleep ${delay}

					# Swipe up to ensure the screen stays on
					# We can easily exceed 30mins timeout if number of iterations is 5
					# on some systems for instance.
					adb -s ${IPADDRESS}:${PORT} shell input touchscreen swipe 200 800 200 700

					adb -s ${IPADDRESS}:${PORT} shell -x 'cmd package compile -m speed-profile -f -a'
				done
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
