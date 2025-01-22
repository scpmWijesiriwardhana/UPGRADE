from brownie import (
    Box,
    TransparentUpgradeableProxy,
    ProxyAdmin,
    config,
    network,
    Contract,
)
from scripts.helpful_scripts import get_account, encode_function_data

def deploy():
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    box = Box.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    print(box.retrieve())


    # # Optional, deploy the ProxyAdmin and use that as the admin contract
    proxy_admin = ProxyAdmin.deploy(
        {"from": account},
    )

    # This will do the same as the above, but with the ProxyAdmin as the admin contract
    # That means that the ProxyAdmin will be able to upgrade the contract
    # This initilizer helps to set the initial value of the Box contract
    initializer=box.store, 1


    # # to simulate the initializer being the `store` function
    # # with a `newValue` of 1
    box_encoded_initializer_function = encode_function_data()

    # # box_encoded_initializer_function = encode_function_data(initializer=box.store, 1)
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    print(f"Proxy deployed to {proxy} ! You can now upgrade it to BoxV2!")
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    proxy_box.store(1, {"from": account})
    print(proxy_box.retrieve())

    return proxy, proxy_admin



def main():
    deploy()