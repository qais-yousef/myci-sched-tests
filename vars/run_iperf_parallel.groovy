def call(bandwidth, duration, num_threads) {
	switch (env.MYCI_NODE_TYPE) {
	case "android":
		if (env.IPADDRESS && env.PORT) {
			sh """
				# Give a chance to whatever other testing
				# running in parallel to start first
				sleep 5

				while true
				do
					#
					# We know we're done when perfetto is no longer running
					# which a sign the other test finished
					# We could replace this with something more deterministic in the future.
					#
					perfetto_running=`adb -s ${IPADDRESS}:${PORT} shell -x 'ps -e | grep perfetto'`
					if [ "x\$perfetto_running" == "x" ]; then
						break
					fi

					#
					# Run iperf
					#
					adb -s ${IPADDRESS}:${PORT} shell "iperf3 -s -D"
					adb -s ${IPADDRESS}:${PORT} shell "iperf3 -c localhost -u -b ${bandwidth} -t ${duration} -i 1 -P ${num_threads}"
					adb -s ${IPADDRESS}:${PORT} shell "pkill -9 iperf3"

					sleep 1
				done
			"""
		} else {
			error "Missing IPADDRESS and/or PORT info"
		}
		break
	case "linux":
		sh """
			# Give a chance to whatever other testing
			# running in parallel to start first
			sleep 5

			while true
			do
				#
				# We know we're done when perfetto is no longer running
				# which a sign the other test finished
				# We could replace this with something more deterministic in the future.
				#
				perfetto_running=`ps -e | grep tracebox || true`
				if [ "x\$perfetto_running" == "x" ]; then
					break
				fi

				#
				# Run iperf
				#
				iperf -s -D
				iperf -c localhost -u -b ${bandwidth} -t ${duration} -i 1 -P ${num_threads}
				pkill -9 iperf

				sleep 1
			done
		"""
		break
	default:
		break
	}
}
