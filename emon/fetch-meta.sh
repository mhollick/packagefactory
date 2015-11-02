#!/bin/bash
#set -x

: <<'END'
A script to set environmental variables as pulled from AWS metadata.
Also, to create a details file containing same variables
for consumption by configuration management tools.
END

DETAILS="details"
EC2_META="ec2-metadata"
emon_config=0

if hash ${EC2_META} 2>/dev/null; then
  ${EC2_META} -d > ${DETAILS}
  export emon_config=1
elif [[ -s ${DETAILS} ]]; then
  #echo "not on aws, boo hoo"
  #echo "already configured"
  export emon_config=2
else
  #echo "not on aws, boo hoo"
  #echo "not configured"
  echo 'service=test' >> ${DETAILS}
  echo 'environment=test' >> ${DETAILS}
  echo 'role=test' >> ${DETAILS}
  echo 'metricshost=' >> ${DETAILS}
  echo 'loghost=' >> ${DETAILS}
  echo 'startmeup=false' >> ${DETAILS}
  export emon_config=3
fi

. ${DETAILS}

if [[ ${emon_config} -gt 0 ]]; then
  #given that we are configured
  #check that there are some essentials set inside details file
  #if there are not, set some half helpful defaults and exit
  # dont start things up
  if ! host ${metricshost} &> /dev/null; then
    echo "Metrics host not set. Cowardly refusing to continue."
    exit 1
  elif ! host ${loghost} &> /dev/null; then
    echo "Log host not set. Cowardly refusing to continue."
    exit 1
  fi
  for thisvar in service environment role; do
    eval tmpvar=\$$thisvar
    echo --$thisvar = $tmpvar--
    if [[ -z ${tmpvar} ]]; then
      echo "${thisvar} was not configured"
      sed -i "/^${thisvar}/d" ${DETAILS}
      echo "${thisvar}=test" >> ${DETAILS}
    fi
  done
  if [[ -z ${location} ]]; then
    if hash ${EC2_META} 2>/dev/null; then
      ${EC2_META} -z | awk '{ print "location=" $2 }' >> ${DETAILS}
    else 
      echo "location=lhc" >> ${DETAILS}
    fi
  fi
fi
