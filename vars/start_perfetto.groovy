def call(name, configs="") {
	if (!env.COLLECT_PELT) {
		env.COLLECT_PELT = 'false'
	}

	if (!env.COLLECT_UCLAMP) {
		env.COLLECT_UCLAMP = 'false'
	}

	switch (env.MYCI_NODE_TYPE) {
	case "android":
		if (env.ANDROID_SERIAL) {
			sh """
				# Cleanup any potential leftover run..
				adb shell -x "killall perfetto"
				sleep 3

				# Create our own directory to store perfetto-trace and clean any potential leftover
				adb shell "mkdir -p /data/misc/perfetto-traces/myci/"
				adb shell "rm -f /data/misc/perfetto-traces/myci/*.perfetto-trace"

				configs="${configs}"

				if [ "${COLLECT_PELT}" == "true" ]; then
					configs="\$configs pelt"
				fi

				if [ "${COLLECT_UCLAMP}" == "true" ]; then
					configs="\$configs uclamp"
				fi

				for config in \$configs
				do
					cat ./tools/config.pbtx.\$config >> ./tools/config.pbtx
				done

				cat ./tools/config.pbtx | adb shell \
					perfetto -d -c - --txt -o /data/misc/perfetto-traces/myci/${name}.perfetto-trace

			"""
		} else {
			error "Missing ANDROID_SERIAL"
		}
		break
	case "linux":
		sh """
			# Cleanup any potential leftover run..
			kill -TERM `cat perfetto.pid` || true
			sleep 3

			configs="${configs}"

			if [ "${COLLECT_PELT}" == "true" ]; then
				configs="\$configs pelt"
			fi

			if [ "${COLLECT_UCLAMP}" == "true" ]; then
				configs="\$configs uclamp"
			fi

			for config in \$configs
			do
				cat ./tools/config.pbtx.\$config >> ./tools/config.pbtx
			done

			touch ${name}.perfetto-trace
			tracebox -o ${name}.perfetto-trace --txt -d -c ./tools/config.pbtx &> perfetto.pid
		"""
		break
	default:
		break
	}
}
