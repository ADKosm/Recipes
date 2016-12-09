Vagrant.configure("2") do |config|
	config.vm.box = "ubuntu/trusty64"

	config.vm.network "forwarded_port", guest: 3000, host: 9001, auto_correct: true
	config.vm.synced_folder "Recipes", "/var/Recipes"
	config.vm.network "forwarded_port", guest: 5432, host: 15432
end
