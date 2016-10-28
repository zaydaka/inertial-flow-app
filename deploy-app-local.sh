sep='--------'
echo $sep"Moving app files to server location"$sep
sudo cp -r /var/www/app/app/inertial-flow-app/* /var/www/app/app
echo $sep"Reloading apache server"$sep
sudo service apache2 reload
