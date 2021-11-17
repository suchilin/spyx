from flask import (render_template, redirect, url_for,
                   request, current_app,abort)
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import login_manager
from . import hitmen_bp
from .forms import SignupForm, LoginForm
from app.auth.models import User


@hitmen_bp.route("/hitmen/", methods=["GET"])
@login_required
def list():
    #  if current_user.is_authenticated:
    #      return redirect(url_for('public.index'))
    hitmen=[]
    if(current_user.id==1):
        hitmen=User.get_all()
    elif(current_user.lackeys):
        hitmen=current_user.lackeys
    else:
        abort(403)
    return render_template("hitmen/list.html",title="Hitmen",hitmen=hitmen)

@hitmen_bp.route("/hitmen/<int:hitman_id>", methods=["GET","POST"])
@login_required
def detail(hitman_id):
    if(current_user.id!=1):
        if hitman_id not in [x.id for x in current_user.lackeys]:
            abort(403)
    message=None
    if(current_user.id==1 or current_user.lackeys):
        hitman=User.get_by_id(hitman_id)
        if(request.method=="POST"):
            save_lackeys=request.form.get("save-lackeys")
            new_lackeys=request.form.getlist("lackeys")
            inactive = request.form.get("inactive-hitman")
            if inactive:
                hitman.active=False
                hitman.save()
                message="Hitman inactived succefully"
            if save_lackeys:
                for l in hitman.lackeys:
                    l.manager=None
                    l.save()
                for nl in new_lackeys:
                    new_lackey=User.get_by_id(nl)
                    new_lackey.manager=hitman
                    new_lackey.save()
                if new_lackeys:
                    message="Lackeys added succefully"
                else:
                    message="Please add some lackeys to hitman"
                if not hitman.active:
                    message="Saved data succefully"
        lackeys = [x.id for x in hitman.lackeys]
        posible_lackeys=[]
        for h in User.get_all():
            if(
                h.id not in lackeys
                and h.id !=1
                and h.id !=hitman.id
                and len(h.lackeys)==0
            ):
                posible_lackeys.append(h)
        return render_template(
            "hitmen/detail.html",
            title="Hitmen",
            hitman=hitman,
            posible_lackeys=posible_lackeys,
            message=message
        )
    else:
        abort(403)
