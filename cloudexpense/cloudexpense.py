#!/usr/bin/python
##-------------------------------------------------------------------
## File : cloudexpense.py
## Author : Denny <contact@dennyzhang.com>
## Description :
## --
## Created : <2017-05-22>
## Updated: Time-stamp: <2017-09-04 18:59:14>
##-------------------------------------------------------------------
from cloudexpense_digitalocean import digitalocean_list_vm, digitalocean_list_volumes
from cloudexpense_linode import linode_list_vm

def cloudexpense(arg_list):
    [digitalocean_token, linode_token, skip_vm_patterns, skip_volumes_patterns] = arg_list
    sum_price = 0
    details = ''

    if digitalocean_token != '':
        (total_price, vm_list) = digitalocean_list_vm(digitalocean_token, skip_vm_patterns)
        details = "%s\n\nEstimated Total Monthly VM Cost In %s: $%s.\n%s" % \
                       (details, 'DigitalOcean', total_price, "\n".join(vm_list))
        sum_price = sum_price + total_price

        (total_price, volume_list) = digitalocean_list_volumes(digitalocean_token, skip_volumes_patterns)
        details = "%s\n\nEstimated Total Monthly Volume Cost In %s: $%s.\n%s" % \
                       (details, 'DigitalOcean', total_price, "\n".join(volume_list))
        sum_price = sum_price + total_price

    if linode_token != '':
        # TODO: add log in case REST API hang
        (total_price, vm_list) = linode_list_vm(linode_token, skip_vm_patterns)
        details = "%s\n\nEstimated Total Monthly Cost In %s(Volume costs not included): $%s.\n%s" % \
                       (details, 'Linode', total_price, "\n".join(vm_list))
        sum_price = sum_price + total_price

    # TODO: support more cloud

    summary = "Estimated Total Monthly Cost Using Cloud: $%s." % (sum_price)
    return (summary, details)

################################################################################
## File : cloudexpense.py ends
