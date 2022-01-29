def call() {
	sh """
		state=`adb shell dumpsys power | grep -i wakefulness= | awk -F = '{print \$2}'`

		if [ "\$state" == "Awake" ]; then
			adb shell input keyevent 26
		fi

		if [ -e .myci_android_display_timeout ]; then
			adb shell settings put system screen_off_timeout \$(cat .myci_android_display_timeout)
		fi
	"""
}
