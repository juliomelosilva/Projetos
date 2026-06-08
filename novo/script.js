// =========================
// CENA THREE.JS
// =========================

const scene = new THREE.Scene();

const camera = new THREE.PerspectiveCamera(
75,
window.innerWidth/window.innerHeight,
0.1,
1000
);

const renderer = new THREE.WebGLRenderer({
canvas:document.getElementById('bg'),
alpha:true
});

renderer.setSize(window.innerWidth,window.innerHeight);

camera.position.z = 40;

// =========================
// GALÁXIA DE PARTÍCULAS
// ALTERE A QUANTIDADE AQUI
// =========================

const count = 6000;

const geometry = new THREE.BufferGeometry();
const positions = [];

for(let i=0;i<count;i++){

 const radius = Math.random()*25;
 const angle = radius*0.6;

 positions.push(
 Math.cos(angle)*radius,
 (Math.random()-0.5)*2,
 Math.sin(angle)*radius
 );
}

geometry.setAttribute(
'position',
new THREE.Float32BufferAttribute(positions,3)
);

const material = new THREE.PointsMaterial({
color:'#ff1f5a',
size:0.08
});

const galaxy = new THREE.Points(geometry,material);

scene.add(galaxy);

// =========================
// ANIMAÇÃO
// =========================

function animate(){

 requestAnimationFrame(animate);

 galaxy.rotation.y += 0.002;
 galaxy.rotation.z += 0.001;

 renderer.render(scene,camera);
}

animate();

window.addEventListener('resize',()=>{

 camera.aspect = window.innerWidth/window.innerHeight;
 camera.updateProjectionMatrix();

 renderer.setSize(
 window.innerWidth,
 window.innerHeight
 );

});
