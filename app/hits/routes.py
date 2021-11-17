from flask import (render_template, redirect, url_for,
                   request, current_app,abort)
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from . import hits_bp
from .forms import HitForm
from .models import Hit
from app.auth.models import User


@hits_bp.route("/hits/bulk/", methods=["GET","POST"])
@login_required
def bulk():
    message=""
    hits=[]
    hitmen=[]
    if current_user.id==1:
        hitmen=User.query.filter(User.id>1)
    elif current_user.lackeys:
        hitmen=[x for x in current_user.lackeys ]
    if(current_user.id==1):
        hits=Hit.query.filter(Hit.status=="asigned")
    else:
        for a in current_user.assignments:
            if a.status=="asigned":
                hits.append(a)
        if(current_user.lackeys):
            for lackey in current_user.lackeys:
                for a in lackey.assignments:
                    if a.status=="asigned":
                        hits.append(a)
    if request.method=="POST":
        assignments=request.form.getlist("assignements")
        for a in assignments:
           [hitA,hitmanA] = a.split(",")
           hitAQ=Hit.query.get(hitA)
           hitmanAQ=User.query.get(hitmanA)
           if hitmanAQ.active:
               hitAQ.hitman_id=hitmanA
               hitAQ.save()
        message="Assignes changed succefully"
    return render_template("hits/bulk.html", title="hits",hits=hits,hitmen=hitmen, message=message)

@hits_bp.route("/hits/", methods=["GET"])
@login_required
def list():
    hits=[]
    if(current_user.id==1):
        hits=Hit.query.all()
    else:
        for a in current_user.assignments:
            hits.append(a)
        if(current_user.lackeys):
            for lackey in current_user.lackeys:
                for a in lackey.assignments:
                    hits.append(a)
    return render_template("hits/list.html", title="hits",hits=hits)


@hits_bp.route("/hits/create/", methods=["GET", "POST"])
@login_required
def create():
    if current_user.id != 1:
        print("USER",current_user.id)
        if not current_user.lackeys:
            abort(403)
    form = HitForm()
    hitmen=[]
    if current_user.id==1:
        hitmen=User.query.filter(User.id>1,User.active==True)
    elif current_user.lackeys:
        hitmen=[x for x in current_user.lackeys if x.active ]
    form.assignee.choices=[(x.id, x.name) for x in hitmen]
    if form.validate_on_submit():
        description=form.description.data
        target = form.target.data
        assignee = form.assignee.data
        hit=Hit(description=description,target=target,hitman_id=assignee,creator_id=current_user.id)
        hit.save()
        print("submited",description,target,assignee)
        return redirect(url_for('hits.list'))
    return render_template('hits/create.html', form=form)

@hits_bp.route("/hits/<int:hit_id>/", methods=["GET", "POST"])
@login_required
def detail(hit_id):
    message=""
    hit = Hit.query.get_or_404(hit_id)
    if current_user.id!=1:
        if current_user.id != hit.hitman.manager.id and current_user.id != hit.hitman.id:
            abort(403)
    hitmen=[]
    if current_user.id==1:
        hitmen=User.query.filter(User.id>1)
    elif current_user.lackeys:
        hitmen=current_user.lackeys
    temphitmen=[]
    for hm in hitmen:
        if hm.active == False:
            if hm.id == hit.hitman.id:
                temphitmen.append(hm)
        else:
            temphitmen.append(hm)
    hitmen=temphitmen
    if request.method=="POST":
        status=request.form.get("status")
        assignee = request.form.get("assignee")
        if status in ("success","failed"):
            hit.status=status
            hit.save()
            message="Ended hit succefully"
        if assignee and assignee != current_user.id:
            hassigne=User.get_by_id(assignee)
            if hassigne.active:
                hit.hitman_id=assignee
                message="Change assignee succefully"
                hit.save()
            else:
                message="You can't assign to inactive user"
    return render_template('hits/detail.html', hit=hit,hitmen=hitmen, message=message)
