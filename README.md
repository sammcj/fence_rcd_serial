## Fencing agent for rcd_serial devices and pacemaker

A Python rewrite of John Sutton's delayed serial STONITH device for use with Pacemaker clusters.

I've been struggling to find a definition of how the agents must be structured / how they're called etc... i.e. does a template / MVP exist etc... so this is *very much untested at present*

- Device: https://smcleod.net/rcd-stonith/
- Related RedHat Bug: https://bugzilla.redhat.com/show_bug.cgi?id=1240868

![](https://smcleod.net/images/san/rcd_serial.jpg)
![](https://smcleod.net/images/san/optoCircuit.jpg)
