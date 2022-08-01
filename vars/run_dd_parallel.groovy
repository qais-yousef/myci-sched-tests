def call(filesize) {
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
					# Run dd
					#
					file="/data/myci.dd.file"
					adb -s ${IPADDRESS}:${PORT} shell "dd if=/dev/zero  of=\$file bs=1M count=${filesize}"
					adb -s ${IPADDRESS}:${PORT} shell "rm -f \$file"

					sleep 3
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
				# Run dd
				#
				file="/tmp/myci.dd.file"
				dd if=/dev/zero  of=\$file bs=1M count=${filesize}
				rm -f \$file

				sleep 3
			done
		"""
		break
	default:
		break
	}
}
