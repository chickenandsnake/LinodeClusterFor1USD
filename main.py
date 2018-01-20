import linode
from linode import  Type, Image, Region

from settings import API_KEY

def create_linode(api_key, image: str, name: str,  ram: int = 1024, cpus: int = 1):
    client = linode.LinodeClient(api_key)
    im_id = client.get_images(linode.Image.label == image)[0].id
    image = Image(client, im_id)
    nodename = client.linode.get_types(Type.memory == ram, Type.vcpus == cpus)[0].id
    region = Region(client, 'eu-west-1a').id
    type = linode.Type(client, nodename)
    l, pw = client.linode.create_instance(type, region, image=image)
    l.label = name
    l.save()
    return dict(name=l.label, ip=l.ipv4[0], passwd=pw)

if __name__ == '__main__':

    NODES = 10
    node_details =[]
    for num in range(1, NODES + 1):
        try:
            node = create_linode(api_key=API_KEY,
                                          image='Ubuntu 16.04 LTS',
                                          name='Node{}'.format(num),
                                          ram=1024,
                                          cpus=1)
            node_details.append(node)
        except linode.ApiError as e:
            print(f"Something went wrong: {e}")

    print(node_details)