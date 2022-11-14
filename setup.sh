echo "Starting the reminder install script..."

userchange="F"

echo "Does reminder user/group exist?"
if ! cat /etc/passwd | grep reminder > /dev/null; then
  echo "  no: Creating reminder user..."
  if useradd --no-create-home --system --base-dir /var/local --shell /usr/sbin/nologin --user-group reminder > /dev/null; then
    echo "    Done"
  else
    echo "    Something went wrong...";
    exit
  fi
  userchange="T"
else
  echo "  yes: nothing to do"
fi

echo "Are users members of the reminder group"
for u in $(ls /home); do
echo "  $u:"
  if ! groups $u | grep reminder > /dev/null; then
    echo "    no: Adding to group"
    if usermod -aG reminder $u > /dev/null; then
      echo "        Added"
    else
      echo "        Something went wrong..."
      exit
    fi
  userchange="T"
  else
    echo "    yes: nothing to do"
  fi
done

echo "Does Event List Directory exist?"
if [ ! -d /var/local/reminder ]; then
  echo "  no: Creating Directory"
  mkdir /var/local/reminder
  chmod 774 /var/local/reminder
  echo -e "#open\n#closed\n#single" > /var/local/reminder/temp.el
  chown --recursive reminder:reminder /var/local/reminder
  chmod 664 /var/local/reminder/temp.el
else
  echo "  yes: nothing to do"
fi

cd /usr/local/bin
echo "Creating symlink to reminder"
if cp -s $OLDPWD/reminder reminder; then
  echo "  Done"
else
  echo "  Something went wrong..."
fi

chmod 755 reminder
cd $OLDPWD

echo "Installation Complete!!!"
if [ "$userchange" = "T" ]; then
  echo
  echo "Restart required for changes to effect."
  read -a answer -p "Restart? (Y/n)"
  if [ -z "$answer" -o "$answer" = "Y" -o "$answer" = "y" ]; then
    reboot 5
  fi
fi
