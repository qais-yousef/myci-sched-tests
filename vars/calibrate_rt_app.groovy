def call() {
	sh """
		pload=`uclampset -m 1024 rt-app ./rt-app/calibration.json 2>&1 | grep "pLoad =" | awk '{print \$5}' | sed 's/ns//'`

		for file in rt-app/*
		do
			sed -i "s/CALIBRATION_VAL/\$pload/" \$file
			cat \$file
		done

		rm -f *-0.log
	"""
}
