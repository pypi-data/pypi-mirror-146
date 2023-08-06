from arpeggio.cleanpeg import NOT, prefix
import pulumi
from resources import ec2


def SEC_GRP(stem, props, vpc_id=None, er=None, ir=None, provider=None, parent=None, depends_on=None):
    # Create Security Group
    sg = ec2.SecurityGroup(
        stem,
        props, 
        vpc_id=vpc_id,
        parent=parent,
        depends_on=depends_on,
        provider=provider
    )

    # Create Security Group Egress Rules
    sg_er = [ec2.SecurityGroupRule(
        stem, 
        props, 
        sg_id=sg.id,
        type='egress',
        from_port=er[i]['from_port'],
        to_port=er[i]['to_port'],
        protocol=er[i]['protocol'],
        cidr=er[i]['cidr_blocks'],
        description=er[i]['description'],
        count=i,
        parent=parent,
        depends_on=depends_on,
        provider=provider
    )
    for i in range(len(er))
    ]

    # Create Security Group Ingress Rules
    sg_ir = [ec2.SecurityGroupRule(
        stem, 
        props, 
        sg_id=sg.id,
        type='ingress',
        from_port=ir[i]['from_port'],
        to_port=ir[i]['to_port'],
        protocol=ir[i]['protocol'],
        cidr=ir[i]['cidr_blocks'],
        description=ir[i]['description'],
        count=i,
        parent=parent,
        depends_on=depends_on,
        provider=provider
    )
    for i in range(len(ir))
    ]

    return sg

    


