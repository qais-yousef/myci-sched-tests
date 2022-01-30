def call() {
	switch (env.MYCI_NODE_TYPE) {
	case "android":
		if (env.IPADDRESS && env.PORT) {
			sh """
				#
				# Kill perfetto process to dump the trace
				#
				adb -s ${IPADDRESS}:${PORT} shell -x "killall perfetto"

				#
				# Make sure trace dump has finished before pulling the file
				#
				TRACE_F=`adb -s ${IPADDRESS}:${PORT} shell "find /data/misc/perfetto-traces/myci -name '*.perfetto-trace'"`

				size_a=0
				size_b=0
				while true
				do
					size_a=`adb -s ${IPADDRESS}:${PORT} shell "ls -l \$TRACE_F" | awk '{print \$5}'`

					if [ \$size_a -eq \$size_b ]; then
						break
					fi

					if [ \$size_b -ne 0 ]; then
						sleep 3
					fi

					size_b=\$size_a
				done

				#
				# We are ready, pull!
				#
				adb -s ${IPADDRESS}:${PORT} pull \$TRACE_F

				#
				# Don't leave leftovers..
				#
				adb -s ${IPADDRESS}:${PORT} shell rm \$TRACE_F
			"""
		} else {
			error "Missing IPADDRESS and/or PORT info"
		}
		break
	case "linux":
		sh """
			kill -TERM `cat perfetto.pid`
		"""
		break
	default:
		break
	}
}
