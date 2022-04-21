def call() {
	switch (env.MYCI_NODE_TYPE) {
	case "android":
		if (env.IPADDRESS && env.PORT) {
			sh """
				# Give a chance to whatever other testing
				# running in parallel to start first
				sleep 5

				i=1
				while true
				do
					#
					# We know we're done when perfetto is no longer running
					# which a sign the other test finished
					# We could replace this with something more deterministic in the future.
					#
					# We will essentially bail out as soon as we observe that. Potentially (likely)
					# leaving dex2oat process still running.
					#
					# TODO: find a way to force dex2oat to exit without rebooting the phone.
					#
					perfetto_running=`adb -s ${IPADDRESS}:${PORT} shell -x 'ps -e | grep perfetto'`
					if [ "x\$perfetto_running" == "x" ]; then
						break
					fi

					#
					# Run dex2oat if not already started.
					#
					stop=5
					for count in \$(seq \$stop)
					do
						dex2oat_running=`adb -s ${IPADDRESS}:${PORT} shell -x 'ps -e | grep dex2oat'`
						if [ "x\$dex2oat_running" == "x" ]; then

							if [ \$count -eq \$stop ]; then
								echo "Iteration [\$i]"
								((i+=1))
								adb -s ${IPADDRESS}:${PORT} shell -x 'cmd package compile -m speed-profile -f -a' &
							else
								sleep 1
							fi
						else
							break
						fi
					done

					sleep \$((5-\$count))
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
