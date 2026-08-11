    real_home = match["score"]["fullTime"]["home"]
    real_away = match["score"]["fullTime"]["away"]

    user = prediction["username"]

    if user == "admin":
        continue

    earned_points = points(
        prediction["home_pred"],
        prediction["away_pred"],
        real_home,
        real_away
    )

    if user not in ranking:

        ranking[user] = {
            "points": 0,
            "exact": 0,
            "correct": 0
        }

    ranking[user]["points"] += earned_points
