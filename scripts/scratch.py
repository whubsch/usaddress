from src.usaddress import parse, tag, trailing_zeros
import usaddress as us
import timeit

# a = tag("123 Main St. Suite 100 Chicago, IL")
# print(a[0])
# print(type(a[0]))

print(parse("1775 Broadway And 57th, New york NY"))
print(parse("123 Main St. Suite 100 Chicago, IL"))

# print(
#     timeit.timeit(
#         'us.tag("123 Main St. Suite 100 Chicago, IL")',
#         setup="from __main__ import us",
#         number=10000,
#     )
# )
# print(
#     timeit.timeit(
#         'tag("123 Main St. Suite 100 Chicago, IL")',
#         setup="from __main__ import tag",
#         number=10000,
#     )
# )
