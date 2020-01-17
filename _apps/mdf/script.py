from mdf_forge.forge import Forge



# You don't have to use the name "mdf" but we do for consistency.
import ipdb; ipdb.set_trace()
mdf = Forge("mdf-test")





mdf.match_field("dc.publisher", "PFHub")

rslt= mdf.search()

for r in rslt:

    print(r)
    import ipdb; ipdb.set_trace()
