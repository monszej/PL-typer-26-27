def points(ph,pa,rh,ra):
    if ph==rh and pa==ra:return 3
    pred=(ph>pa)-(ph<pa)
    real=(rh>ra)-(rh<ra)
    return 1 if pred==real else 0
