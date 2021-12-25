echo(version=version());

scale=1.25;
foot=0.5;
module game_piece(t=0){
    color("green")
    rotate_extrude($fn = 200)
    polygon( points=scale*[[0,10],[2,10],[3,9],[4.666,4],[5.5,3],[7,3],[7,-foot],[5.75,-foot],[5.75,0],[4,3],[2.5,7.5],[0,7.5]] );
}
//game_piece();
projection(cut = true) rotate([90,0,0]) game_piece();

//projection(cut = true) rotate([90,0,0]) translate(scale*[0, 0, 3+foot]) game_piece();

// alternative
//points=[[0,9],[2,9],[3,8],[4.666,3],[5.5,2],[7,2],[7,-1.1],[6,-1.1],[6,1],[5,1],[4,2],[2.333,7],[1.5,8],[0,8]]