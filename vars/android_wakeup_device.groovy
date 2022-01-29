def call() {
	sh """
		state=`adb shell dumpsys power | grep -i wakefulness= | awk -F = '{print \$2}'`

		if [ "\$state" != "Awake" ]; then
			adb shell input keyevent 26
			sleep 1
			adb shell input touchscreen swipe 200 800 200 100
		fi

		# Set timeout to 30 mins if not already set to that
		timeout=`adb shell settings get system screen_off_timeout`

		if [ "\$timeout" != "1800000" ]; then
			adb shell settings put system screen_off_timeout 1800000
			echo \$timeout > .myci_android_display_timeout
		fi
	"""
}
