def call(name, configs="") {
	if (!env.COLLECT_PELT) {
		env.COLLECT_PELT = 'false'
	}

	if (!env.COLLECT_UCLAMP) {
		env.COLLECT_UCLAMP = 'false'
	}

	if (!env.COLLECT_RQ_PRESSURE) {
		env.COLLECT_RQ_PRESSURE = 'false'
	}

	switch (env.MYCI_NODE_TYPE) {
	case "android":
		if (env.IPADDRESS && env.PORT) {
			sh """
				# Cleanup any potential leftover run..
				adb -s ${IPADDRESS}:${PORT} shell -x "killall perfetto"
				sleep 3

				# Create our own directory to store perfetto-trace and clean any potential leftover
				adb -s ${IPADDRESS}:${PORT} shell "mkdir -p /data/misc/perfetto-traces/myci/"
				adb -s ${IPADDRESS}:${PORT} shell "rm -f /data/misc/perfetto-traces/myci/*.perfetto-trace"

				configs="${configs}"

				if [ "${COLLECT_PELT}" == "true" ]; then
					configs="\$configs pelt"
				fi

				if [ "${COLLECT_UCLAMP}" == "true" ]; then
					configs="\$configs uclamp"
				fi

				if [ "${COLLECT_RQ_PRESSURE}" == "true" ]; then
					configs="\$configs rq_pressure"
				fi

				for config in \$configs
				do
					cat ./tools/config.pbtx.\$config >> ./tools/config.pbtx
				done

				cat ./tools/config.pbtx | adb -s ${IPADDRESS}:${PORT} shell \
					perfetto -d -c - --txt -o /data/misc/perfetto-traces/myci/${name}.perfetto-trace

			"""
		} else {
			error "Missing IPADDRESS and/or PORT info"
		}
		break
	case "linux":
		sh """
			# Cleanup any potential leftover run..
			pkill -TERM tracebox || true
			sleep 3

			configs="${configs}"

			if [ "${COLLECT_PELT}" == "true" ]; then
				configs="\$configs pelt"
			fi

			if [ "${COLLECT_UCLAMP}" == "true" ]; then
				configs="\$configs uclamp"
			fi

			if [ "${COLLECT_RQ_PRESSURE}" == "true" ]; then
				configs="\$configs rq_pressure"
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
