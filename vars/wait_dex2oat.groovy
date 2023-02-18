def call() {
	switch (env.MYCI_NODE_TYPE) {
	case "android":
		if (env.ANDROID_SERIAL) {
			sh """
				counter=0
				stop=5
				while true
				do
					running=`adb shell -x 'ps -e | grep dex2oat'`

					if [ "x\$running" == "x" ]; then
						((counter+=1))
					else
						counter=0
					fi

					if [ \$counter -eq \$stop ]; then
						break
					fi

					sleep 1
				done
			"""
		} else {
			error "Missing ANDROID_SERIAL"
		}
		break
	case "linux":
	default:
		error "Only supported on Android"
		break
	}
}
