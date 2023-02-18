def call() {
	switch (env.MYCI_NODE_TYPE) {
	case "android":
		if (env.ANDROID_SERIAL) {
			sh """
				#
				# Kill perfetto process to dump the trace
				#
				adb shell -x "killall perfetto"

				#
				# Make sure trace dump has finished before pulling the file
				#
				TRACE_F=`adb shell "find /data/misc/perfetto-traces/myci -name '*.perfetto-trace'"`

				size_a=0
				size_b=0
				while true
				do
					size_a=`adb shell "ls -l \$TRACE_F" | awk '{print \$5}'`

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
				retry=5
				for i in \$(seq \$retry)
				do
					if [ \$i -eq \$retry ]; then
						# Make sure to propagate the failure on last retry
						adb pull \$TRACE_F
					else
						adb pull \$TRACE_F || true
					fi

					if [ -e *.perfetto-trace ]; then
						break
					fi

					sleep 3

					status=`adb devices | grep ${ANDROID_SERIAL} | awk '{print \$2}'`
					if [ "x\$status" == "xoffline" ]; then
						adb reconnect offline
					fi
				done

				#
				# Don't leave leftovers..
				#
				adb shell rm \$TRACE_F
			"""
		} else {
			error "Missing ANDROID_SERIAL"
		}
		break
	case "linux":
		sh """
			kill -TERM `cat perfetto.pid` || true
		"""
		break
	default:
		break
	}
}
