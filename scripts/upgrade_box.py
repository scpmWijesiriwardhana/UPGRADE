#!/usr/bin/python3
from brownie import (
    BoxV2,
    TransparentUpgradeableProxy,
    ProxyAdmin,
    config,
    network,
    Contract,
)
from scripts.helpful_scripts import get_account, upgrade
from scripts.deploy_box import deploy


def main():
    proxy, proxy_admin = deploy()
    account = get_account()
    print(f"Deploying to {network.show_active()}")
    box_v2 = BoxV2.deploy(
        {"from": account},
        publish_source=config["networks"][network.show_active()]["verify"],
    )
    
    
    upgrade_tx = upgrade(account, proxy, box_v2, proxy_admin_contract=proxy_admin)
    upgrade_tx.wait(1)
    print("Proxy has been upgraded!")


    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    print(f"Starting value {proxy_box.retrieve()}")
    tx_inc = proxy_box.increment({"from": account})
    tx_inc.wait(1)
    print(f"Ending value {proxy_box.retrieve()}")
