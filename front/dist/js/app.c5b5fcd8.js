(function(t){function e(e){for(var a,i,o=e[0],c=e[1],u=e[2],l=0,f=[];l<o.length;l++)i=o[l],Object.prototype.hasOwnProperty.call(n,i)&&n[i]&&f.push(n[i][0]),n[i]=0;for(a in c)Object.prototype.hasOwnProperty.call(c,a)&&(t[a]=c[a]);d&&d(e);while(f.length)f.shift()();return r.push.apply(r,u||[]),s()}function s(){for(var t,e=0;e<r.length;e++){for(var s=r[e],a=!0,o=1;o<s.length;o++){var c=s[o];0!==n[c]&&(a=!1)}a&&(r.splice(e--,1),t=i(i.s=s[0]))}return t}var a={},n={app:0},r=[];function i(e){if(a[e])return a[e].exports;var s=a[e]={i:e,l:!1,exports:{}};return t[e].call(s.exports,s,s.exports,i),s.l=!0,s.exports}i.m=t,i.c=a,i.d=function(t,e,s){i.o(t,e)||Object.defineProperty(t,e,{enumerable:!0,get:s})},i.r=function(t){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(t,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(t,"__esModule",{value:!0})},i.t=function(t,e){if(1&e&&(t=i(t)),8&e)return t;if(4&e&&"object"===typeof t&&t&&t.__esModule)return t;var s=Object.create(null);if(i.r(s),Object.defineProperty(s,"default",{enumerable:!0,value:t}),2&e&&"string"!=typeof t)for(var a in t)i.d(s,a,function(e){return t[e]}.bind(null,a));return s},i.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return i.d(e,"a",e),e},i.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)},i.p="/";var o=window["webpackJsonp"]=window["webpackJsonp"]||[],c=o.push.bind(o);o.push=e,o=o.slice();for(var u=0;u<o.length;u++)e(o[u]);var d=c;r.push([0,"chunk-vendors"]),s()})({0:function(t,e,s){t.exports=s("56d7")},"1e6d":function(t,e,s){},2586:function(t,e,s){"use strict";var a=s("38b4"),n=s.n(a);n.a},"38b4":function(t,e,s){},"4c5c":function(t,e,s){},"56d7":function(t,e,s){"use strict";s.r(e);s("e260"),s("e6cf"),s("cca6"),s("a79d");var a=s("2b0e"),n=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("router-view")},r=[],i=(s("5c0b"),s("2877")),o={},c=Object(i["a"])(o,n,r,!1,null,null,null),u=c.exports,d=s("8c4f"),l=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{attrs:{id:"app"}},[s("header",[s("topbar",{attrs:{round:t.round,roundProgress:t.roundProgress,timer:t.timer}})],1),s("container",[s("statuses"),s("scoreboard",{attrs:{updateRound:t.updateRound,updateRoundTime:t.updateRoundTime,updateRoundStart:t.updateRoundStart,timer:t.timer}})],1),t._m(0)],1)},f=[function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("footer",{staticClass:"footer"},[t._v(" Scoreboard adapted from the "),s("a",{attrs:{href:"https://github.com/pomo-mondreganto/ForcAD"}},[t._v("ForcAD")]),t._v(" project by "),s("span",{staticClass:"team"},[t._v("C4T BuT S4D")]),t._v(" CTF team ")])}],m=(s("0d03"),s("4795"),s("96cf"),s("1da1")),v=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"container"},[t._t("default")],2)},p=[],h=(s("989d"),{}),_=Object(i["a"])(h,v,p,!1,null,"2788e5c9",null),b=_.exports,g=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"topbar"},[s("div",{staticClass:"progress-bar",style:{width:t.roundProgressInteger}}),s("div",{staticClass:"tp"},[t._v("Round: "+t._s(t.round))])])},C=[],k=(s("a9e3"),{props:{round:Number,timer:Number,roundProgress:Number},computed:{roundProgressInteger:function(){return"".concat(Math.floor(100*this.roundProgress),"%")}},methods:{go:function(){clearInterval(this.timer)}}}),x=k,y=(s("e563"),Object(i["a"])(x,g,C,!1,null,"7d32cf86",null)),S=y.exports,T=function(){var t=this,e=t.$createElement,s=t._self._c||e;return null!==t.error?s("div",[t._v(t._s(t.error))]):null!==t.teams?s("div",{staticClass:"table"},[s("div",{staticClass:"row"},[s("div",{staticClass:"number"},[t._v("#")]),s("div",{staticClass:"team-logo-col"},[t._v("logo")]),s("div",{staticClass:"team"},[t._v("team")]),s("div",{staticClass:"score"},[t._v("score")]),s("div",{staticClass:"service-name"},t._l(t.tasks,(function(e){var a=e.name,n=e.stores,r=e.firstBloods;return s("div",{key:a,staticClass:"service-cell"},[t._v(" "+t._s(a)+" "),s("div",{staticClass:"first-bloods"},t._l(n,(function(e){return s("div",{key:e,staticClass:"firstblood-cell"},[r[e]?s("i",{staticClass:"fas fa-tint blood"}):t._e(),s("span",{class:[r[e]?"blood":""]},[t._v(" "+t._s(r[e]?t.teamNameByIndex(r[e].TeamId):"Flagstore #"+e+" unexploited")+" ")])])})),0)])})),0)]),s("transition-group",{attrs:{name:"teams-list"}},t._l(t.teams,(function(e,a){var n=e.name,r=e.score,i=e.tasks,o=e.ip,c=e.id,u=e.highlighted;return s("div",{key:n,staticClass:"row",class:["top-"+(a+1),u?"highlighted":""]},[s("div",{staticClass:"number",class:["top-"+(a+1),a>2?"default-team":"",u?"pd-3-left":"",u?"pd-3-topbottom":""]},[t._v(" "+t._s(a+1)+" ")]),s("div",{staticClass:"team-logo-col"},[t.teamLogoByIndex(c)?s("img",{staticClass:"team-logo",attrs:{src:t.teamLogoByIndex(c)}}):t._e()]),s("div",{staticClass:"team team-row",class:["top-"+(a+1),a>2?"default-team":"",u?"pd-3-topbottom":""],on:{click:function(e){return t.openTeam(c)}}},[s("div",{staticClass:"team-name"},[t.teamFlagByIndex(c)?s("img",{staticClass:"team-flag",attrs:{src:t.teamFlagByIndex(c)}}):t._e(),t._v(" "+t._s(n))]),s("div",{staticClass:"ip"},[t._v(t._s(t.getDnsSuffix()?"team"+c+"."+t.getDnsSuffix():o))])]),s("div",{staticClass:"score",class:["top-"+(a+1),a>2?"default-team":"",u?"pd-3-topbottom":""]},[t._v(" "+t._s(r.toFixed(2))+" ")]),s("div",{staticClass:"service"},t._l(i,(function(e){var a=e.id,n=e.sla,r=e.attack,o=e.defense,c=e.message,u=e.status;return s("div",{key:a,staticClass:"service-cell",class:"status-"+u,style:{"font-size":1-i.length/20+"em"}},[c?s("button",{staticClass:"info"},[s("i",{staticClass:"fas fa-info-circle"}),s("span",{staticClass:"tooltip"},[t._v(t._s(""===c?"OK":c))])]):t._e(),s("div",{staticClass:"sla"},[s("i",{staticClass:"fas fa-tachometer-alt"}),t._v(" "+t._s(n.toFixed(2))+" ")]),s("div",{staticClass:"attack"},[s("i",{staticClass:"fas fa-flag"}),t._v(" "+t._s(r.toFixed(2))+" ")]),s("div",{staticClass:"defense"},[s("i",{staticClass:"fas fa-shield-alt"}),t._v(" "+t._s(o.toFixed(2))+" ")])])})),0)])})),0)],1):t._e()},w=[],I=(s("4160"),s("d81d"),s("4e82"),s("b0c0"),s("d3b7"),s("159b"),"");I=window.location.origin;var R=I,O=[101,102,103,104,110,111],P={101:"UP",102:"RECOVERING",103:"MUMBLE",104:"DOWN",110:"CHECK FAILED",111:"INACTIVE","-1":"OFFLINE"},E=s("d4ec"),j=s("bee2"),F=function(){function t(e){var s=this,a=e.ServiceName,n=e.ServiceId,r=e.MaxStores,i=e.FirstBloods;Object(E["a"])(this,t),this.name=a,this.id=n,this.stores=r,this.firstBloods={},i.forEach((function(t){s.firstBloods[t.StoreIndex+1]=t}))}return Object(j["a"])(t,null,[{key:"comp",value:function(t,e){return t.id-e.id}}]),t}(),N=F,$=(s("caad"),s("2532"),s("b85c")),B=function(){function t(e){var s=e.ServiceId,a=e.ServiceStatus,n=e.ServiceLevelAgreementPoints,r=e.AttackPoints,i=e.LostDefensePoints,o=e.Message;Object(E["a"])(this,t),this.id=s+100*n+1e4*r+1e6*i,this.taskId=s,this.status="INACTIVE"===a?111:"OK"===a?101:"RECOVERING"===a?102:"MUMBLE"===a?103:"OFFLINE"===a?104:110,this.sla=n,this.attack=r,this.defense=i,this.message=o}return Object(j["a"])(t,null,[{key:"comp",value:function(t,e){return t.taskId-e.taskId}}]),t}(),D=B,L=function(){function t(e,s){Object(E["a"])(this,t);var a=e.Name,n=e.TeamId;this.name=a,this.id=n,this.ip="10.0.0."+n,this.taskModels=s,this.update(e)}return Object(j["a"])(t,[{key:"update",value:function(t){if(t.TeamId==this.id){this.score=t.TotalPoints,this.attack=t.AttackPoints,this.defense=t.LostDefensePoints,this.sla=t.ServiceLevelAgreementPoints,this.tasks=t.ServiceDetails.map((function(t){return new D(t)}));var e,s=this.tasks.map((function(t){return t.taskId})),a=Object($["a"])(this.taskModels);try{for(a.s();!(e=a.n()).done;){var n=e.value;s.includes(n.id)||this.tasks.push(new D({ServiceId:n.id,ServiceLevelAgreementPoints:0,AttackPoints:0,LostDefensePoints:0,message:""}))}}catch(r){a.e(r)}finally{a.f()}this.tasks.sort(D.comp)}}}],[{key:"comp",value:function(t,e){return e.score-t.score}}]),t}(),M=L,A=s("bc3a"),U=s.n(A),K={props:{updateRound:Function,updateRoundTime:Function,updateRoundStart:Function,timer:Number},data:function(){return{error:null,server:null,tasks:null,teams:null,round_start:0}},methods:{openTeam:function(t){clearInterval(this.timer),this.$router.push({name:"team",params:{id:t}})["catch"]((function(){}))},teamNameByIndex:function(t){var e="";return this.teams.forEach((function(s){s.id==t&&(e=s.name)})),e},teamFlagByIndex:function(t){return this.config.Teams[t]?this.config.Teams[t]["FlagUrl"]:null},teamLogoByIndex:function(t){return this.config.Teams[t]?this.config.Teams[t]["LogoUrl"]:null},getDnsSuffix:function(){return this.config.DnsSuffix}},created:function(){var t=Object(m["a"])(regeneratorRuntime.mark((function t(){var e,s,a,n,r,i,o,c,u,d,l,f,m,v,p=this;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:if(e){t.next=14;break}return t.prev=1,t.next=4,U.a.get("".concat(R,"/api/config"));case 4:return e=t.sent,t.abrupt("break",14);case 8:return t.prev=8,t.t0=t["catch"](1),t.next=12,new Promise((function(t){return setTimeout(t,2e3)}));case 12:t.next=0;break;case 14:this.config=e.data,this.config.Title&&(document.title="".concat(this.config.Title," Scoreboard"));case 16:if(s){t.next=30;break}return t.prev=17,t.next=20,U.a.get("".concat(R,"/api/scoreboard"));case 20:return s=t.sent,t.abrupt("break",30);case 24:return t.prev=24,t.t1=t["catch"](17),t.next=28,new Promise((function(t){return setTimeout(t,2e3)}));case 28:t.next=16;break;case 30:a=s.data,n=a.CurrentRound,r=a.StartTimeEpoch,i=a.EndTimeEpoch,o=a.Services,c=a.Teams,this.updateRoundStart(i),this.updateRoundTime(i-r),this.updateRound(n),this.tasks=o.map((function(t){return new N(t)})).sort(N.comp),this.teams=c.map((function(t){return new M(t,p.tasks)})).sort(M.comp);case 36:if(!this.teams){t.next=56;break}return t.prev=37,t.next=40,U.a.get("".concat(R,"/api/scoreboard/live"));case 40:s=t.sent,u=s.data,d=u.CurrentRound,l=u.StartTimeEpoch,f=u.EndTimeEpoch,m=u.Services,v=u.Teams,this.updateRoundStart(f),this.updateRoundTime(f-l),this.updateRound(d),this.tasks=m.map((function(t){return new N(t)})).sort(N.comp),v.forEach((function(t){p.teams.forEach((function(e){e.update(t)}))})),this.teams=this.teams.sort(M.comp),t.next=54;break;case 50:return t.prev=50,t.t2=t["catch"](37),t.next=54,new Promise((function(t){return setTimeout(t,2e3)}));case 54:t.next=36;break;case 56:case"end":return t.stop()}}),t,this,[[1,8],[17,24],[37,50]])})));function e(){return t.apply(this,arguments)}return e}()},V=K,z=(s("b99b"),Object(i["a"])(V,T,w,!1,null,"5162dd24",null)),G=z.exports,J=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{staticClass:"statuses"},t._l(t.statuses,(function(e){return s("div",{key:e,staticClass:"status-cell",class:"status-"+e},[t._v(" "+t._s(t.statusesNames[e])+" ")])})),0)},H=[],W={data:function(){return{statuses:O,statusesNames:P}}},q=W,Q=(s("2586"),Object(i["a"])(q,J,H,!1,null,"4069afa5",null)),X=Q.exports,Y={components:{Container:b,Topbar:S,Scoreboard:G,Statuses:X},data:function(){return{round:0,roundStart:0,timer:null,roundTime:null,roundProgress:null}},created:function(){var t=Object(m["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:this.timer=setInterval(this.tick,500);case 1:case"end":return t.stop()}}),t,this)})));function e(){return t.apply(this,arguments)}return e}(),methods:{updateRound:function(t){this.round=t},updateRoundTime:function(t){this.roundTime=t},updateRoundStart:function(t){this.roundStart=t},tick:function(){null===this.roundTime||null===this.roundStart||this.round<1?this.roundProgress=0:(this.roundProgress=((new Date).getTime()/1e3-this.roundStart)/this.roundTime,this.roundProgress=Math.min(this.roundProgress,1))}}},Z=Y,tt=(s("5ad5"),Object(i["a"])(Z,l,f,!1,null,"1fb68286",null)),et=tt.exports,st=function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("div",{attrs:{id:"app"}},[s("header",[s("topbar",{attrs:{round:t.round}})],1),s("container",[s("statuses"),s("team-scoreboard",{attrs:{updateRound:t.updateRound}})],1),t._m(0)],1)},at=[function(){var t=this,e=t.$createElement,s=t._self._c||e;return s("footer",{staticClass:"footer"},[t._v(" Powered by "),s("span",{staticClass:"team"},[t._v("C4T BuT S4D")]),t._v(" CTF team ")])}],nt=function(){var t=this,e=t.$createElement,s=t._self._c||e;return null!==t.error?s("div",[t._v(" "+t._s(t.error)+" ")]):null!==t.team?s("div",{staticClass:"table"},[s("div",{staticClass:"row"},[s("div",{staticClass:"number"},[t._v("#")]),s("div",{staticClass:"team"},[t._v("team")]),s("div",{staticClass:"score"},[t._v("score")]),s("div",{staticClass:"service-name"},t._l(t.tasks,(function(e){var a=e.name;return s("div",{key:a,staticClass:"service-cell"},[t._v(" "+t._s(a)+" ")])})),0)]),s("div",t._l(t.states,(function(e,a){return s("div",{key:a,staticClass:"row"},[s("div",{staticClass:"number"},[t._v(" "+t._s(e.round)+" ")]),s("div",{staticClass:"team"},[s("div",{staticClass:"team-name"},[t._v(t._s(t.team.name))]),s("div",{staticClass:"ip"},[t._v(t._s(t.team.ip))])]),s("div",{staticClass:"score"},[t._v(" "+t._s(e.score.toFixed(2))+" ")]),s("div",{staticClass:"service"},t._l(e.tasks,(function(e){var a=e.id,n=e.sla,r=e.attack,i=e.defense,o=e.message,c=e.status;return s("div",{key:a,staticClass:"service-cell",class:"status-"+c,style:{"font-size":1-t.tasks.length/20+"em"}},[o?s("button",{staticClass:"info"},[s("i",{staticClass:"fas fa-info-circle"}),s("span",{staticClass:"tooltip"},[t._v(t._s(""===o?"OK":o))])]):t._e(),s("div",{staticClass:"sla"},[s("i",{staticClass:"fas fa-tachometer-alt"}),t._v(" "+t._s(n.toFixed(2))+" ")]),s("div",{staticClass:"attack"},[s("i",{staticClass:"fas fa-flag"}),t._v(" "+t._s(r.toFixed(2))+" ")]),s("div",{staticClass:"defense"},[s("i",{staticClass:"fas fa-shield-alt"}),t._v(" "+t._s(i.toFixed(2))+" ")])])})),0)])})),0)]):t._e()},rt=[],it=(s("99af"),s("4de4"),s("13d5"),{props:{updateRound:Function,updateRoundStart:Function},data:function(){return{error:null,team:null,teamId:null,tasks:null,round:0,by_task:[]}},created:function(){var t=Object(m["a"])(regeneratorRuntime.mark((function t(){var e,s,a,n,r=this;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return this.teamId=this.$route.params.id,t.prev=1,t.next=4,this.$http.get("".concat(R,"/api/scoreboard"));case 4:return e=t.sent,s=e.data,t.next=8,this.$http.get("".concat(R,"/api/teams/").concat(this.teamId));case 8:a=t.sent,n=a.data,this.team=new M(s.Teams.filter((function(t){var e=t.TeamId;return e==r.teamId}))[0],[]),this.tasks=s.Services.sort((function(t,e){var s=t.ServiceId,a=e.ServiceId;return s-a})).map((function(t){return{name:t.ServiceName}})),this.round=n.reduce((function(t,e){var s=e.Round;return Math.max(t,s)}),0),this.updateRound(this.round),n=n.map((function(t){return{round:t.Round,score:t.TotalPoints,tasks:t.ServiceDetails.map((function(t){return new D(t)})).sort((function(t,e){var s=t.taskId,a=e.taskId;return s-a}))}})),this.states=n.sort((function(t,e){var s=t.round,a=e.round;return a-s})),t.next=21;break;case 18:t.prev=18,t.t0=t["catch"](1),this.error="Can't connect to server";case 21:case"end":return t.stop()}}),t,this,[[1,18]])})));function e(){return t.apply(this,arguments)}return e}()}),ot=it,ct=(s("e17f"),Object(i["a"])(ot,nt,rt,!1,null,"2f6ffe62",null)),ut=ct.exports,dt={components:{Container:b,Topbar:S,TeamScoreboard:ut,Statuses:X},data:function(){return{round:0}},methods:{updateRound:function(t){this.round=t}}},lt=dt,ft=(s("d2fd"),Object(i["a"])(lt,st,at,!1,null,"bd6848d8",null)),mt=ft.exports;a["a"].use(d["a"]);var vt=[{path:"/",name:"index",component:et},{path:"/team/:id/",name:"team",component:mt}],pt=new d["a"]({mode:"history",base:"/",routes:vt}),ht=pt;a["a"].config.productionTip=!1,U.a.defaults.withCredentials=!0,a["a"].prototype.$http=U.a,ht.$http=U.a,new a["a"]({router:ht,render:function(t){return t(u)}}).$mount("#app")},"5ad5":function(t,e,s){"use strict";var a=s("7d8f"),n=s.n(a);n.a},"5c0b":function(t,e,s){"use strict";var a=s("9c0c"),n=s.n(a);n.a},"7d8f":function(t,e,s){},"989d":function(t,e,s){"use strict";var a=s("d3e3"),n=s.n(a);n.a},"9c0c":function(t,e,s){},a107:function(t,e,s){},b99b:function(t,e,s){"use strict";var a=s("1e6d"),n=s.n(a);n.a},d2fd:function(t,e,s){"use strict";var a=s("4c5c"),n=s.n(a);n.a},d32f:function(t,e,s){},d3e3:function(t,e,s){},e17f:function(t,e,s){"use strict";var a=s("a107"),n=s.n(a);n.a},e563:function(t,e,s){"use strict";var a=s("d32f"),n=s.n(a);n.a}});
//# sourceMappingURL=app.c5b5fcd8.js.map