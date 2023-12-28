import flask
import ipaddress
import secrets

app = flask.Flask(__name__)
# secret key needed to flash messages
app.secret_key = secrets.token_hex()


@app.route('/', methods=['GET', 'POST'])
def index():
    if flask.request.method == 'GET':
        return flask.render_template('index.html', show_table=False)
    if flask.request.method == 'POST':
        input_cidr = flask.request.form['cidr']
        try:
            cidr = ipaddress.ip_network(input_cidr, strict=False)
        except ValueError as e:
            flask.flash('Not a valid CIDR')
            return flask.render_template('index.html', input_cidr=input_cidr, show_table=False)

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
        private_public = "Private" if cidr.is_private else "Public"
        # version = cidr.version
        in_addr_arpa = ip_address.reverse_pointer
        ipv4_mapped = ip_address.ipv4_mapped

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
            'private_public': private_public,
            'in_addr_arpa': in_addr_arpa,
            'ipv4_mapped': ipv4_mapped,
            # 'version': version,
        }

        return flask.render_template('index.html', input_cidr=input_cidr, data=data)


@app.route('/gibmeip')
def gibmeip():
    client_ip = flask.request.access_route[-1]
    return f'Access Route: {str(flask.request.access_route)}\nRemote Addr: {str(flask.request.remote_addr)}'
    # return f'{client_ip}'


# catch all route
@app.route('/<path:path>')
def catch_all(path):
    return flask.redirect(flask.url_for('index'))
