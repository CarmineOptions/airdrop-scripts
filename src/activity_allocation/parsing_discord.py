# Most of the work to get the testnet role and OG role addresses was manual,
# here are just some helper code snippets to speed up the manual process

# OGs
# Processing OGs was almost only manual (just a few addresses)
addresses = []
users = []
for line in text.split('\n'):
	if '0x' in line:
		addresses.append(line)
	if '2023' in line:
		users.append(line.split(' ')[0])

prev_line = ''
for line in text.split('\n'):
	if '0x' in line and len(line) < 66:
		print(line, ' ', prev_line)
	prev_line = line


# ##################################
# Testnet
addresses = {}  # {'user': [address, address,...]}
prev_line = ''
for line in text.split('\n'):
	if '0x' in line and '2023' in prev_line and 'Marek' not in prev_line:
		user = prev_line.split('/')[0][:-5]
		for add in [x for x in line.split(' ') if '0x' in x]:
			if user not in addresses:
				addresses[user] = []
			addresses[user].append(add)
	prev_line = line

## NO NEED TO MANUALLY RESOLVE
for user, addrs in addresses.items():
	if len(addrs) == 1 and len(addrs[0]) > 45:
		print(addrs[0])
		
## NEED TO REMIND USERS TO PROVIDE STARKNET ADDRESS
for user, addrs in addresses.items():
	if len(addrs) == 1 and len(addrs[0]) < 45:
		print(user)
        # and MoonChild | Suiswap ['0x8FaA1037767993aAB590d54f13391c85F59A193e', '0x8FaA1037767993aAB590d54f13391c85F59A193e']

## NEED MANUAL PROCESSING
for user, addrs in addresses.items():
	if len(addrs) > 1:
		print(user, addrs)

# Manual
0x0757c7d2124FC9B5F34a6a19659aC6522C3B48d5467A50b672cA5463237915CB
0x00a3277903655d57bd33c5215360078f7924d0868a9a235780dce22ef5dd9edf
0x04BC57Ece59927e1a16ee601b2eD5D3cc4B64786c0C110eAb847b409E34033f3
0x0342ffc4691e1dfa2e098742db1bff0ab0bfe027aea115f3df664d0494cbb991
0x0379111a951e5c356394e049a9720ba7c45e96c9b86a69d513df5a6fb47dcebe
0x076f85f77d65969d3d5254b79dc4be2047a7e025b1d4ed19d17c95ea05df946a
0x19da7bda3b0e6cc4ef532edc52dda9bc59718dec37d0ba65e804f370bf99c52
0x048833c018f3F581a38D48BA5f6D46C66B18eb1633EEfF37ff70b274c287CB60
0x065B7eFBb72B3809cb47630cC8e8E3bd7bB909Be1C9F7A6F2aFA2c5465937309
0x038a24b08d9eac18c46b2315126ba1c341836ad46a4b56c76bae66935e73d737
0x01519BfF2E8A17451A9511b79718E93a487DF12E59EF21F7e2e514EBe36e95B4
0x06203be11405d743d85375899d7030a681ad6a508ebe4553c2a8d1c4a4df762f
0x00e2e310fdc6d7cb057b96494274f9638f3928c2444a2cb8351d2e5295a1f812
0x07657EEb175A5d3B51c5abFa2cd73B367da8F0Ebc4b3a7c1804F77e8b30b1ff4
0x025d73f56B37336306729E41d93ebE16361b8723F5cC56e25978185C042447b9
0x026eeDDAd2347a4e468Cc0c7d3941a8DE7b59d2d17D9dE8de0A5347a0fE6c620
0x06AE56D65F2c80921D75b7F16aBBE8F2982F050A875C4029CDdF2ed40614442b
0x02ef794e979123225e3cdb251ccb63281e213f6ae81c4313e91940e489c73bd4
0x04b5f07ca8e14f670c2b2de2ff2b28349c44efd5e5ec14cde82ed3a5b7ad986a
0x05585e3288bbfa24c18ef490fb15542b8192108b9ee4ac6afb019a6a5fe6f3dc
0x0169664a5c44e5d25b2b2ac0137c9255183816b063fc4db15aff93bd5e600330
0x0119777513a7b45d71b012830ad7794321e7d8afd93d34fc380f7c74e2ed1705
0x0096c1203291e2a2a08fe46d473a55f05fe2900adaf14e8ec834fe685d0dea6b
0x00848e78110e11a68b7d4fe3b63176bc77b768c2db301a1929c518b24a507a32
0x00ae0b6cceac871df19cb68c20f36a3a9d72640c227fe509efbd856b7bf7f306
0x0062d46feeafe820701054f65b321bffeca4b2c6d4c04816ce62527a400e95f2
0x029832ce7634275b9ffde20b106a2247d1668efa6ef094f1b588be2ac13d3d86
0x016d8660a90fc9bc8f583b38572721b2a9477aa6d586de285ab57211dff6fdb3
0x02a032ce5afca72a61bc64451472d29d55ca5dfc27f661fffb343935d5162672
0x0765f0b94b4f7756bf1a724b3dcb2e92329afea40f84f7223f704395f84f535a
0x0339cc6843f65b5c9dd2c4f465066ae4d737a3ed52e50b3831f4abe86da205dd
0x07ff38a2632f492a556c7b2a3cf7da60bf7003208df5442e2184313facb5ac38
0x06140a06c0cf8062ce2cf6a7466b24ed9d97ca4e2b5d73b8e338fb158f4ea485
0x01db903225f17d098d172d5d9ca07339524e7936f713ae285a85cd4deb266993
0x00733e46fd94b1896448f11dd99e6a8a737bf6856662ced317b0ba4d439e4a1b
0x01c2b5e1db08d5efea5829a156a85a2b632cd075a480892a17a34448f3008feb
0x062c3e99fc6d65cda2de822374be5419de676a3152d0a52dc251fefb8535b03a
0x01879516530bad2151eaa6bb56b5c5b756b0bd184fe6764c6a3ee40d4dd7ee9c
0x0589661d5ae354b07e2ca49e7b1b3d5ff589e8f8be0d2809288be3dcd0622451
0x05427ca801c0f0a0bd1ea933773ff6c0bb960558381e2849347b6cd15ac89e59
0x0322bde671aa6d35276e1aec8e8132a03a39d0b1370d4b9834645776e0b9d22a
0x0536c4f08ff5f88992e16a87e08f77bca06b149354892bddc97dbbb28239c867
0x0602ab64407c797f8ba806de89c3ee839e40d18393454adf12935037a5a112cb
0x03f09e5f67f693bf6143f98311dcf26aebe2681a3703fe26d5ba88b9f188a900
0x061e4790e9089a1c475fb947223d64648f518cbc34a409db9aa21f5238e282de
0x06059a21107451b5fa4fcfd059f58080c03f3b2e50a616a1e11e840ab37e0fd8


