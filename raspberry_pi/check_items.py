def check_items(closet, status):
	for clothing in closet:
		if clothing.is_checked_in == status:
			clothing.print()
	
