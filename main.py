from flask import Flask
import flask
import ipaddress
from pprint import pprint
import secrets

app = Flask(__name__)

app.secret_key = secrets.token_hex()


def get_class(ip):
    first_octet = int(str(ip).split('.')[0])
    if 1 <= first_octet <= 126:
        return 'Class A'
    elif 128 <= first_octet <= 191:
        return 'Class B'
    elif 192 <= first_octet <= 223:
        return 'Class C'
    elif 224 <= first_octet <= 239:
        return 'Class D'
    elif 240 <= first_octet <= 255:
        return 'Class E'
    else:
        return 'Invalid IP'


@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'GET':
        return flask.render_template('index.html', data='')
    if flask.request.method == 'POST':
        try:
            cidr = ipaddress.ip_network(
                flask.request.form['cidr'], strict=False)
        except ValueError as e:
            flask.flash('Not a valid CIDR')
            return flask.render_template('index.html', data='')

        input_cidr = flask.request.form['cidr']
        ip_address = ipaddress.ip_address(
            flask.request.form['cidr'].split('/')[0])
        network_address = cidr.network_address

        if cidr.num_addresses <= 2:
            usable_address_range = 'N/A'
        else:
            usable_address_range = "{} - {}".format(
                cidr[1], cidr[-2])
        broadcast_address = cidr.broadcast_address
        total_num_hosts = cidr.num_addresses
        num_usable_hosts = 0 if int(
            total_num_hosts - 2) < 0 else int(total_num_hosts - 2)
        subnet_mask = cidr.netmask
        binary_subnet_mask = bin(int(subnet_mask))[2:]
        chunks = [binary_subnet_mask[i:i+8]
                  for i in range(0, len(binary_subnet_mask), 8)]
        binary_subnet_mask = '.'.join(chunks)
        ip_class = None
        private_public = "Private" if cidr.is_private else "Public"
        # version = cidr.version
        in_addr_arpa = ip_address.reverse_pointer
        ipv4_mapped = None
        _6to4_prefix = None

        data = {
            'input_cidr': input_cidr,
            'ip_address': ip_address,
            'cidr': cidr,
            'network_address': network_address,
            'usable_address_range': usable_address_range,
            'broadcast_address': broadcast_address,
            'total_num_hosts': total_num_hosts,
            'num_usable_hosts': num_usable_hosts,
            'subnet_mask': subnet_mask,
            'binary_subnet_mask': binary_subnet_mask,
            'ip_class': ip_class,
            'private_public': private_public,
            'in_addr_arpa': in_addr_arpa,
            'ipv4_mapped': ipv4_mapped,
            # 'version': version,
        }

        pprint(data)
        return flask.render_template('index.html', data=data)


app.run(debug=True, host="0.0.0.0", port=8080)
