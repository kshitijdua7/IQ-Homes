/* ==========================================================================
   IQ Homes — interactive 3D smart home
   A procedurally built cutaway house with live device hotspots.
   No external assets: every mesh, texture and glow is generated at runtime.
   ========================================================================== */

import * as THREE from 'three';
import { EffectComposer } from './vendor/postprocessing/EffectComposer.js';
import { RenderPass } from './vendor/postprocessing/RenderPass.js';
import { UnrealBloomPass } from './vendor/postprocessing/UnrealBloomPass.js';
import { ShaderPass } from './vendor/postprocessing/ShaderPass.js';
import { OutputPass } from './vendor/postprocessing/OutputPass.js';

/* ---------- Brand palette ------------------------------------------------ */
const C = {
  navy:      0x0b2545,
  navyDark:  0x081a33,
  navyDeep:  0x050d1a,
  teal:      0x17d7c2,
  tealDim:   0x0e9f8c,
  blue:      0x2e8bff,
  floor:     0x14335a,
  wall:      0x3f6ea8,
  furniture: 0x1b3a63,
  furnAlt:   0x244a7a,
  warm:      0xffd9a0
};

/* ---------- The devices we light up -------------------------------------- */
const DEVICES = [
  {
    id: 'lock',
    name: 'Smart Locks & Keyless Entry',
    blurb: 'Unlock with your phone, a code or your voice. Grant a cleaner or a guest their own access — and see exactly who came and went.',
    pos: [0.62, 1.05, 2.56],
    room: 'hall'
  },
  {
    id: 'doorbell',
    name: 'Video Doorbell',
    blurb: 'See and speak to whoever is at your door from anywhere. Packages, visitors and deliveries all recorded to your phone.',
    pos: [1.30, 1.42, 2.56],
    room: 'hall'
  },
  {
    id: 'camera',
    name: '24/7 Security Cameras',
    blurb: 'Crisp day-and-night coverage of every approach to your home, with motion alerts that tell the mail carrier from a stranger.',
    pos: [-3.25, 5.18, 2.28],
    room: 'exterior'
  },
  {
    id: 'lighting',
    name: 'Voice-Controlled Lighting',
    blurb: '"Movie night." Lights dim, the room warms, the rest of the house drops to a soft glow. One phrase, every fixture.',
    pos: [-1.85, 2.32, 0.15],
    room: 'living'
  },
  {
    id: 'theatre',
    name: 'Home Theatre & Whole-Home Audio',
    blurb: 'Cinema picture and properly tuned sound in the living room, with music that follows you room to room.',
    pos: [-3.28, 1.45, 0.35],
    room: 'living'
  },
  {
    id: 'climate',
    name: 'Smart Climate Control',
    blurb: 'Your home learns your schedule and warms up before you get in. Room-by-room comfort, and a visibly smaller gas bill.',
    pos: [-0.44, 1.55, 1.55],
    room: 'hall'
  },
  {
    id: 'blinds',
    name: 'Motorized Blinds & Curtains',
    blurb: 'Blinds that lift with the sunrise and close at dusk. Silent, wire-free, and controllable from bed.',
    pos: [-2.05, 4.05, 2.56],
    room: 'bedroom'
  },
  {
    id: 'garage',
    name: 'Garage Door Control',
    blurb: 'Never wonder whether you left it open. Check from anywhere, close it with a tap, and let it open as you pull in.',
    pos: [2.95, 1.15, 1.28],
    room: 'garage'
  },
  {
    id: 'hub',
    name: 'One App. One Voice.',
    blurb: 'Whole-home mesh Wi-Fi and a single control hub tying every system together — so it is one app, not eleven.',
    pos: [0.55, 2.95, 0.55],
    room: 'hub'
  }
];

/* ---------- Small helpers ------------------------------------------------ */
const box = (w, h, d) => new THREE.BoxGeometry(w, h, d);

function mesh(geo, mat, x, y, z, parent) {
  const m = new THREE.Mesh(geo, mat);
  m.position.set(x, y, z);
  if (parent) parent.add(m);
  return m;
}

/** Radial-gradient sprite texture used for every glow in the scene. */
function glowTexture() {
  const s = 128;
  const cv = document.createElement('canvas');
  cv.width = cv.height = s;
  const ctx = cv.getContext('2d');
  const g = ctx.createRadialGradient(s / 2, s / 2, 0, s / 2, s / 2, s / 2);
  g.addColorStop(0.00, 'rgba(255,255,255,1)');
  g.addColorStop(0.18, 'rgba(23,215,194,0.95)');
  g.addColorStop(0.45, 'rgba(23,215,194,0.35)');
  g.addColorStop(1.00, 'rgba(23,215,194,0)');
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, s, s);
  const t = new THREE.CanvasTexture(cv);
  t.colorSpace = THREE.SRGBColorSpace;
  return t;
}

/* --------------------------------------------------------------------------
   The scan sweep.

   The reference effect fakes depth on a flat photo with a depth map. Here the
   geometry is genuinely 3D, so the scan can run through real world-space
   height instead — a dot-matrix band that climbs the house and lights up
   whatever surface it passes through. Shared uniforms so every patched
   material moves as one.
   -------------------------------------------------------------------------- */
const scanUniforms = {
  uScanY:       { value: -2 },
  uScanWidth:   { value: 0.42 },
  uScanDensity: { value: 6.0 },
  uScanColor:   { value: new THREE.Color(0xff2f52) },
  uScanBoost:   { value: new THREE.Color(0x17d7c2) },
  uScanOn:      { value: 1 }
};

const SCAN_VERT_HEAD = 'varying vec3 vScanWP;\n';
const SCAN_VERT_BODY = `#include <begin_vertex>
  vScanWP = ( modelMatrix * vec4( transformed, 1.0 ) ).xyz;`;

const SCAN_FRAG_HEAD = `
varying vec3 vScanWP;
uniform float uScanY;
uniform float uScanWidth;
uniform float uScanDensity;
uniform vec3  uScanColor;
uniform vec3  uScanBoost;
uniform float uScanOn;
float iqCellHash( vec2 p ) {
  return fract( sin( dot( p, vec2( 127.1, 311.7 ) ) ) * 43758.5453123 );
}
`;

const SCAN_FRAG_BODY = `#include <dithering_fragment>
  {
    float band = 1.0 - smoothstep( 0.0, uScanWidth, abs( vScanWP.y - uScanY ) );
    if ( band > 0.001 ) {
      // Dot matrix laid out in world space, so it sticks to the building
      vec2 grid  = vScanWP.xz * uScanDensity;
      vec2 cell  = fract( grid ) - 0.5;
      float dots = smoothstep( 0.44, 0.26, length( cell ) );
      float bright = 0.35 + iqCellHash( floor( grid ) ) * 1.15;
      float lead = smoothstep( 0.55, 1.0, band );
      vec3 tint = mix( uScanColor, uScanBoost, lead * 0.55 );
      gl_FragColor.rgb += tint * band * dots * bright * 1.7 * uScanOn;
      // A soft wash so flat surfaces still register the pass
      gl_FragColor.rgb += uScanColor * pow( band, 3.0 ) * 0.22 * uScanOn;
    }
  }`;

/** Patches a standard material so the scan sweep runs through it. */
function enableScan(mat) {
  mat.onBeforeCompile = shader => {
    Object.assign(shader.uniforms, scanUniforms);
    shader.vertexShader = SCAN_VERT_HEAD +
      shader.vertexShader.replace('#include <begin_vertex>', SCAN_VERT_BODY);
    shader.fragmentShader = SCAN_FRAG_HEAD +
      shader.fragmentShader.replace('#include <dithering_fragment>', SCAN_FRAG_BODY);
  };
  // Without this three would hand back a cached, unpatched program
  mat.customProgramCacheKey = () => 'iq-scan-v1';
  return mat;
}

/** Adds a teal edge outline around a geometry — the "architectural" look. */
function addEdges(geo, parent, x, y, z, opacity = 0.34) {
  const lines = new THREE.LineSegments(
    new THREE.EdgesGeometry(geo, 25),
    new THREE.LineBasicMaterial({ color: C.teal, transparent: true, opacity })
  );
  lines.position.set(x, y, z);
  parent.add(lines);
  return lines;
}

/* ==========================================================================
   Main entry
   ========================================================================== */
export function initHouse(stageEl) {
  if (!stageEl) return;

  const canvas = stageEl.querySelector('canvas');
  const loader = stageEl.querySelector('[data-stage-loader]');
  const hint = stageEl.querySelector('[data-stage-hint]');
  const tip = stageEl.querySelector('[data-stage-tip]');
  const detail = stageEl.querySelector('[data-stage-detail]');
  const detailTitle = stageEl.querySelector('[data-detail-title]');
  const detailBody = stageEl.querySelector('[data-detail-body]');
  const detailClose = stageEl.querySelector('[data-detail-close]');

  /* --- WebGL capability check --- */
  let renderer;
  try {
    renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: true,
      alpha: true,
      powerPreference: 'high-performance'
    });
  } catch (err) {
    stageEl.classList.add('no-webgl');
    return;
  }
  if (!renderer.getContext()) {
    stageEl.classList.add('no-webgl');
    return;
  }

  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const isCoarse = window.matchMedia('(pointer: coarse)').matches;

  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.12;

  const scene = new THREE.Scene();
  scene.fog = new THREE.Fog(C.navyDeep, 20, 40);

  const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 100);
  const target = new THREE.Vector3(0, 2.55, 0);

  /* ---------------------------------------------------------------------
     Materials
     --------------------------------------------------------------------- */
  const matStruct = new THREE.MeshStandardMaterial({
    color: C.navy, roughness: 0.82, metalness: 0.08
  });
  const matFloor = new THREE.MeshStandardMaterial({
    color: C.floor, roughness: 0.68, metalness: 0.12
  });
  const matGlass = new THREE.MeshStandardMaterial({
    color: C.wall, roughness: 0.22, metalness: 0.1,
    transparent: true, opacity: 0.11,
    side: THREE.DoubleSide, depthWrite: false
  });
  const matPartition = new THREE.MeshStandardMaterial({
    color: C.wall, roughness: 0.4, metalness: 0.05,
    transparent: true, opacity: 0.2,
    side: THREE.DoubleSide, depthWrite: false
  });
  const matFurn = new THREE.MeshStandardMaterial({
    color: C.furniture, roughness: 0.75, metalness: 0.05
  });
  const matFurnAlt = new THREE.MeshStandardMaterial({
    color: C.furnAlt, roughness: 0.7, metalness: 0.05
  });
  const matAccent = new THREE.MeshStandardMaterial({
    color: C.tealDim, roughness: 0.4, metalness: 0.2,
    emissive: C.tealDim, emissiveIntensity: 0.25
  });
  const matScreen = new THREE.MeshStandardMaterial({
    color: C.navyDeep, roughness: 0.15, metalness: 0.4,
    emissive: C.blue, emissiveIntensity: 0.55
  });
  const matWindow = new THREE.MeshStandardMaterial({
    color: C.warm, roughness: 0.1, metalness: 0,
    emissive: C.warm, emissiveIntensity: 1.35,
    transparent: true, opacity: 0.62, side: THREE.DoubleSide
  });

  // Every surface the scan should light up as it climbs the building
  [matStruct, matFloor, matGlass, matPartition, matFurn, matFurnAlt].forEach(enableScan);

  const house = new THREE.Group();
  scene.add(house);

  /* ---------------------------------------------------------------------
     Ground platform
     --------------------------------------------------------------------- */
  const platform = new THREE.Mesh(
    new THREE.CylinderGeometry(7.2, 7.4, 0.35, 64),
    new THREE.MeshStandardMaterial({ color: C.navyDeep, roughness: 0.9, metalness: 0.1 })
  );
  platform.position.y = -0.2;
  house.add(platform);

  const rim = new THREE.Mesh(
    new THREE.TorusGeometry(7.22, 0.028, 8, 90),
    new THREE.MeshBasicMaterial({ color: C.teal, transparent: true, opacity: 0.55 })
  );
  rim.rotation.x = Math.PI / 2;
  rim.position.y = -0.02;
  house.add(rim);

  // Faint concentric "signal" rings on the ground — echoes the logo mark
  for (let i = 0; i < 3; i++) {
    const r = 3.1 + i * 1.35;
    const ring = new THREE.Mesh(
      new THREE.TorusGeometry(r, 0.012, 6, 80),
      new THREE.MeshBasicMaterial({ color: C.teal, transparent: true, opacity: 0.16 - i * 0.04 })
    );
    ring.rotation.x = Math.PI / 2;
    ring.position.y = -0.015;
    house.add(ring);
  }

  /* ---------------------------------------------------------------------
     Shell — floors, walls, roof
     Main block  X -3.4 → 1.6   Z -2.5 → 2.5
     Garage      X  1.6 → 4.2   Z -2.5 → 1.2
     --------------------------------------------------------------------- */
  const MX0 = -3.4, MX1 = 1.6, MZ0 = -2.5, MZ1 = 2.5;
  const MW = MX1 - MX0, MD = MZ1 - MZ0;
  const MCX = (MX0 + MX1) / 2, MCZ = (MZ0 + MZ1) / 2;
  const F1 = 2.5;          // ground floor ceiling height
  const SLAB = 0.16;
  const F2 = F1 + SLAB;    // upper floor level
  const TOP = F2 + 2.4;    // upper ceiling
  const T = 0.1;           // wall thickness

  // Ground slab
  const gSlab = box(MW, 0.2, MD);
  mesh(gSlab, matFloor, MCX, -0.1, MCZ, house);

  // Mid slab
  const mSlab = box(MW, SLAB, MD);
  mesh(mSlab, matFloor, MCX, F1 + SLAB / 2, MCZ, house);
  addEdges(mSlab, house, MCX, F1 + SLAB / 2, MCZ, 0.3);

  // Thin ceiling line at the top of the upper floor (kept translucent so the
  // rooms stay visible when the camera is high)
  const ceil = box(MW, 0.06, MD);
  mesh(ceil, matPartition, MCX, TOP + 0.03, MCZ, house);

  /* --- Gabled roof, built as an explicit prism ---------------------------
     A pitched roof is what makes the silhouette read as a *home* rather than
     an office block, so it is worth the handful of vertices. Translucent, with
     a bright teal edge, so the upper floor stays visible from above.        */
  {
    const x0 = MX0 - 0.28, x1 = MX1 + 0.28;
    const zb = MZ0 - 0.28, zf = MZ1 + 0.28, zm = MCZ;
    const y0 = TOP + 0.06, y1 = TOP + 1.5;

    const v = [
      x0, y0, zb,   // 0 A
      x0, y0, zf,   // 1 B
      x0, y1, zm,   // 2 C
      x1, y0, zb,   // 3 D
      x1, y0, zf,   // 4 E
      x1, y1, zm    // 5 F
    ];
    const idx = [
      1, 4, 5,  1, 5, 2,   // front slope
      3, 0, 2,  3, 2, 5,   // back slope
      0, 1, 2,             // left gable
      4, 3, 5              // right gable
    ];
    const g = new THREE.BufferGeometry();
    g.setAttribute('position', new THREE.Float32BufferAttribute(v, 3));
    g.setIndex(idx);
    g.computeVertexNormals();

    const roofMat = new THREE.MeshStandardMaterial({
      color: C.wall, roughness: 0.35, metalness: 0.12,
      transparent: true, opacity: 0.2,
      side: THREE.DoubleSide, depthWrite: false
    });
    house.add(new THREE.Mesh(g, enableScan(roofMat)));

    // Bright ridge + eaves outline
    house.add(new THREE.LineSegments(
      new THREE.EdgesGeometry(g, 15),
      new THREE.LineBasicMaterial({ color: C.teal, transparent: true, opacity: 0.62 })
    ));

    // Solid ridge beam — catches the light and reads as a real roofline
    mesh(box(x1 - x0, 0.09, 0.09), matStruct, (x0 + x1) / 2, y1, zm, house);

    // Chimney
    mesh(box(0.42, 1.0, 0.42), matStruct, MX0 + 1.0, TOP + 0.85, MCZ - 1.15, house);
  }

  // Exterior walls (transparent) — back, left, right, front
  const wallSpecs = [
    { g: box(MW, TOP, T), x: MCX, y: TOP / 2, z: MZ0 - T / 2 },        // back
    { g: box(T, TOP, MD), x: MX0 - T / 2, y: TOP / 2, z: MCZ },        // left
    { g: box(T, TOP, MD), x: MX1 + T / 2, y: TOP / 2, z: MCZ },        // right
    { g: box(MW, TOP, T), x: MCX, y: TOP / 2, z: MZ1 + T / 2 }         // front
  ];
  wallSpecs.forEach(w => {
    mesh(w.g, matGlass, w.x, w.y, w.z, house);
    addEdges(w.g, house, w.x, w.y, w.z, 0.3);
  });

  // Vertical corner posts, solid — gives the shell some weight
  [[MX0, MZ0], [MX1, MZ0], [MX0, MZ1], [MX1, MZ1]].forEach(([x, z]) => {
    mesh(box(0.14, TOP, 0.14), matStruct, x, TOP / 2, z, house);
  });

  /* --- Garage --- */
  const GX0 = 1.6, GX1 = 4.2, GZ0 = -2.5, GZ1 = 1.2;
  const GW = GX1 - GX0, GD = GZ1 - GZ0, GCX = (GX0 + GX1) / 2, GCZ = (GZ0 + GZ1) / 2;
  const GH = 2.5;

  mesh(box(GW, 0.2, GD), matFloor, GCX, -0.1, GCZ, house);
  const gRoof = box(GW + 0.3, 0.2, GD + 0.3);
  mesh(gRoof, matStruct, GCX, GH + 0.1, GCZ, house);
  addEdges(gRoof, house, GCX, GH + 0.1, GCZ, 0.4);
  [
    { g: box(GW, GH, T), x: GCX, y: GH / 2, z: GZ0 - T / 2 },
    { g: box(T, GH, GD), x: GX1 + T / 2, y: GH / 2, z: GCZ }
  ].forEach(w => {
    mesh(w.g, matGlass, w.x, w.y, w.z, house);
    addEdges(w.g, house, w.x, w.y, w.z, 0.28);
  });

  // Garage door — teal panel lines
  const gDoor = box(GW - 0.25, 1.9, 0.08);
  mesh(gDoor, matFurnAlt, GCX, 0.95, GZ1 + 0.04, house);
  for (let i = 0; i < 4; i++) {
    mesh(box(GW - 0.3, 0.02, 0.02), matAccent, GCX, 0.25 + i * 0.46, GZ1 + 0.1, house);
  }

  // A car in the driveway silhouette
  const car = new THREE.Group();
  mesh(box(1.55, 0.42, 0.78), matFurn, 0, 0.34, 0, car);
  mesh(box(0.85, 0.34, 0.72), matFurnAlt, -0.05, 0.68, 0, car);
  [[-0.5, 0.42], [0.5, 0.42], [-0.5, -0.42], [0.5, -0.42]].forEach(([x, z]) => {
    const w = new THREE.Mesh(new THREE.CylinderGeometry(0.17, 0.17, 0.12, 14), matStruct);
    w.rotation.x = Math.PI / 2;
    w.position.set(x, 0.17, z);
    car.add(w);
  });
  mesh(box(0.1, 0.08, 0.6), new THREE.MeshStandardMaterial({
    color: C.warm, emissive: C.warm, emissiveIntensity: 1.1
  }), 0.78, 0.42, 0, car);
  car.position.set(GCX - 0.1, 0, GZ1 + 1.9);
  car.rotation.y = Math.PI / 2;
  house.add(car);

  /* ---------------------------------------------------------------------
     Interior partitions
     --------------------------------------------------------------------- */
  // Ground: living room divider at x = -0.4
  mesh(box(T, F1, MD), matPartition, -0.4, F1 / 2, MCZ, house);
  // Ground: kitchen / hall divider at z = 0.5 (right side only)
  mesh(box(2.0, F1, T), matPartition, 0.6, F1 / 2, 0.5, house);
  // Upper: bedroom divider at x = -0.6
  mesh(box(T, 2.4, MD), matPartition, -0.6, F2 + 1.2, MCZ, house);
  // Upper: bedroom / office split at z = 0.8
  mesh(box(2.8, 2.4, T), matPartition, -2.0, F2 + 1.2, 0.8, house);
  // Upper: bathroom / landing split at z = 0.2
  mesh(box(2.2, 2.4, T), matPartition, 0.5, F2 + 1.2, 0.2, house);

  /* --- Staircase, ground → upper --- */
  const stair = new THREE.Group();
  for (let i = 0; i < 12; i++) {
    mesh(box(0.95, 0.11, 0.24), matFurnAlt, 0, 0.11 + i * 0.215, -i * 0.24, stair);
  }
  stair.position.set(0.55, 0, 2.05);
  house.add(stair);

  /* ---------------------------------------------------------------------
     Furniture
     --------------------------------------------------------------------- */
  // -- Living room (ground left) --
  const rug = new THREE.Mesh(
    new THREE.BoxGeometry(2.5, 0.02, 1.9),
    new THREE.MeshStandardMaterial({ color: C.navyDark, roughness: 0.95 })
  );
  rug.position.set(-1.9, 0.02, 0.3);
  house.add(rug);

  mesh(box(2.05, 0.36, 0.85), matFurnAlt, -1.9, 0.28, 1.15, house);   // sofa seat
  mesh(box(2.05, 0.5, 0.24), matFurnAlt, -1.9, 0.5, 1.5, house);      // sofa back
  mesh(box(0.22, 0.42, 0.85), matFurnAlt, -2.85, 0.42, 1.15, house);  // arm L
  mesh(box(0.22, 0.42, 0.85), matFurnAlt, -0.95, 0.42, 1.15, house);  // arm R
  mesh(box(1.05, 0.08, 0.5), matFurn, -1.9, 0.42, 0.15, house);       // coffee table
  mesh(box(0.06, 0.34, 0.06), matFurn, -2.35, 0.21, 0.15, house);
  mesh(box(0.06, 0.34, 0.06), matFurn, -1.45, 0.21, 0.15, house);

  // TV on the left wall
  mesh(box(0.06, 0.78, 1.4), matScreen, MX0 + 0.12, 1.45, 0.35, house);
  mesh(box(0.09, 0.9, 1.55), matStruct, MX0 + 0.07, 1.45, 0.35, house);
  // Media console + speakers
  mesh(box(0.34, 0.42, 1.6), matFurn, MX0 + 0.25, 0.21, 0.35, house);
  mesh(box(0.2, 0.72, 0.2), matFurn, MX0 + 0.28, 0.36, -0.65, house);
  mesh(box(0.2, 0.72, 0.2), matFurn, MX0 + 0.28, 0.36, 1.35, house);

  // -- Kitchen (ground right-back) --
  mesh(box(1.85, 0.85, 0.55), matFurn, 0.62, 0.42, MZ0 + 0.35, house);   // counter run
  mesh(box(1.85, 0.05, 0.58), matFurnAlt, 0.62, 0.87, MZ0 + 0.35, house); // countertop
  mesh(box(1.15, 0.82, 0.6), matFurn, 0.6, 0.41, -0.75, house);           // island
  mesh(box(1.25, 0.05, 0.7), matFurnAlt, 0.6, 0.85, -0.75, house);
  mesh(box(0.5, 1.5, 0.5), matFurnAlt, 1.25, 0.75, MZ0 + 0.9, house);     // fridge
  // Under-cabinet accent light
  mesh(box(1.7, 0.02, 0.04), matAccent, 0.62, 0.9, MZ0 + 0.62, house);

  // -- Hall / entry (ground right-front) --
  mesh(box(0.06, 0.42, 0.42), matFurnAlt, -0.34, 1.5, 1.55, house);      // thermostat plate
  // Front door
  mesh(box(0.9, 2.0, 0.09), matFurnAlt, 0.62, 1.0, MZ1 + 0.02, house);
  mesh(box(0.08, 0.08, 0.05), matAccent, 0.98, 1.02, MZ1 + 0.09, house); // handle
  // Doorbell housing
  mesh(box(0.1, 0.2, 0.06), matFurn, 1.3, 1.42, MZ1 + 0.06, house);

  // -- Bedroom (upper left-back) --
  mesh(box(1.75, 0.3, 1.95), matFurnAlt, -2.15, F2 + 0.22, -1.2, house);  // bed base
  mesh(box(1.75, 0.16, 1.75), matFurn, -2.15, F2 + 0.44, -1.1, house);    // mattress top
  mesh(box(1.8, 0.62, 0.12), matFurn, -2.15, F2 + 0.5, MZ0 + 0.18, house); // headboard
  mesh(box(0.62, 0.14, 0.36), matFurnAlt, -2.5, F2 + 0.56, -1.85, house); // pillow
  mesh(box(0.62, 0.14, 0.36), matFurnAlt, -1.8, F2 + 0.56, -1.85, house); // pillow
  mesh(box(0.42, 0.46, 0.4), matFurn, -3.05, F2 + 0.3, -2.05, house);     // nightstand
  mesh(box(0.5, 1.6, 0.85), matFurn, MX0 + 0.35, F2 + 0.8, 0.25, house);  // wardrobe

  // -- Office (upper left-front) --
  mesh(box(1.5, 0.07, 0.62), matFurnAlt, -2.3, F2 + 0.75, 1.85, house);   // desk
  mesh(box(0.06, 0.72, 0.06), matFurn, -2.95, F2 + 0.38, 1.85, house);
  mesh(box(0.06, 0.72, 0.06), matFurn, -1.65, F2 + 0.38, 1.85, house);
  mesh(box(0.68, 0.42, 0.04), matScreen, -2.3, F2 + 1.05, 1.62, house);   // monitor
  mesh(box(0.42, 0.42, 0.42), matFurn, -2.3, F2 + 0.42, 2.25, house);     // chair

  // -- Bathroom (upper right-back) --
  mesh(box(1.05, 0.5, 0.62), matFurnAlt, 0.55, F2 + 0.25, MZ0 + 0.5, house); // tub
  mesh(box(0.42, 0.62, 0.36), matFurn, 1.25, F2 + 0.31, -0.35, house);       // vanity

  /* --- Windows: warm emissive panes on the exterior walls --- */
  const winSpecs = [
    // front face (z = MZ1)
    { w: 1.9, h: 1.15, x: -1.9, y: 1.35, z: MZ1 + 0.06, ry: 0 },
    { w: 1.5, h: 1.0,  x: -2.05, y: F2 + 1.15, z: MZ1 + 0.06, ry: 0 },
    { w: 1.2, h: 0.95, x: 0.5,  y: F2 + 1.15, z: MZ1 + 0.06, ry: 0 },
    // left face (x = MX0)
    { w: 1.5, h: 1.0,  x: MX0 - 0.06, y: F2 + 1.2, z: -1.3, ry: Math.PI / 2 },
    // back face (z = MZ0)
    { w: 1.6, h: 1.05, x: 0.5, y: 1.35, z: MZ0 - 0.06, ry: 0 },
    { w: 1.4, h: 1.0,  x: -2.1, y: F2 + 1.2, z: MZ0 - 0.06, ry: 0 }
  ];
  winSpecs.forEach(s => {
    const p = new THREE.Mesh(new THREE.PlaneGeometry(s.w, s.h), matWindow);
    p.position.set(s.x, s.y, s.z);
    p.rotation.y = s.ry;
    house.add(p);
    const fr = new THREE.Mesh(
      new THREE.EdgesGeometry(new THREE.PlaneGeometry(s.w, s.h)),
      new THREE.LineBasicMaterial({ color: C.teal, transparent: true, opacity: 0.5 })
    );
    fr.position.copy(p.position);
    fr.rotation.y = s.ry;
    house.add(fr);
  });

  // Motorized blind slats over the upper front window
  const blind = new THREE.Group();
  for (let i = 0; i < 5; i++) {
    mesh(box(1.5, 0.05, 0.03), matFurnAlt, 0, i * 0.1, 0, blind);
  }
  blind.position.set(-2.05, F2 + 1.55, MZ1 + 0.1);
  house.add(blind);

  /* ---------------------------------------------------------------------
     Lighting
     --------------------------------------------------------------------- */
  scene.add(new THREE.HemisphereLight(0xa8dcff, 0x0d2340, 0.9));
  scene.add(new THREE.AmbientLight(0x8fb4e0, 0.7));

  const key = new THREE.DirectionalLight(0xeaf6ff, 2.1);
  key.position.set(7, 11, 8);
  scene.add(key);

  const fillTeal = new THREE.DirectionalLight(C.teal, 0.85);
  fillTeal.position.set(-8, 4, -6);
  scene.add(fillTeal);

  const fillBlue = new THREE.DirectionalLight(C.blue, 0.6);
  fillBlue.position.set(4, 2, -9);
  scene.add(fillBlue);

  // Per-room lamps that brighten when the matching hotspot is hovered
  const roomLights = {
    living:  new THREE.PointLight(C.warm, 3.2, 8, 2),
    hall:    new THREE.PointLight(C.warm, 2.2, 6.5, 2),
    bedroom: new THREE.PointLight(C.warm, 2.6, 7, 2),
    kitchen: new THREE.PointLight(C.warm, 2.0, 6, 2),
    office:  new THREE.PointLight(0xcfe6ff, 1.8, 6, 2),
    garage:  new THREE.PointLight(0xbfe4ff, 1.4, 6, 2),
    hub:     new THREE.PointLight(C.teal, 2.4, 9, 2),
    exterior:new THREE.PointLight(C.teal, 1.4, 9, 2)
  };
  roomLights.living.position.set(-1.9, 2.1, 0.3);
  roomLights.hall.position.set(0.55, 2.1, 1.4);
  roomLights.bedroom.position.set(-2.1, F2 + 2.0, -1.0);
  roomLights.kitchen.position.set(0.6, 2.1, -1.2);
  roomLights.office.position.set(-2.2, F2 + 2.0, 1.8);
  roomLights.garage.position.set(GCX, 2.1, GCZ);
  roomLights.hub.position.set(0.55, 2.95, 0.55);
  roomLights.exterior.position.set(-3.0, 5.0, 2.0);
  Object.values(roomLights).forEach(l => {
    l.userData.base = l.intensity;
    scene.add(l);
  });

  /* ---------------------------------------------------------------------
     Hotspots
     --------------------------------------------------------------------- */
  const glowTex = glowTexture();
  const hotspots = [];

  DEVICES.forEach((d, i) => {
    const g = new THREE.Group();
    g.position.set(d.pos[0], d.pos[1], d.pos[2]);

    const sprite = new THREE.Sprite(new THREE.SpriteMaterial({
      map: glowTex,
      transparent: true,
      opacity: 0.85,
      depthWrite: false,
      depthTest: false,
      blending: THREE.AdditiveBlending
    }));
    sprite.scale.setScalar(0.72);
    g.add(sprite);

    const core = new THREE.Mesh(
      new THREE.SphereGeometry(0.075, 16, 12),
      new THREE.MeshBasicMaterial({ color: 0xffffff })
    );
    core.renderOrder = 2;
    core.material.depthTest = false;
    g.add(core);

    // Generous, invisible hit target
    const hit = new THREE.Mesh(
      new THREE.SphereGeometry(0.32, 10, 8),
      new THREE.MeshBasicMaterial({ transparent: true, opacity: 0, depthWrite: false })
    );
    hit.userData.index = i;
    g.add(hit);

    house.add(g);
    hotspots.push({ ...d, group: g, sprite, core, hit, phase: i * 0.7, hovered: false, active: false });
  });

  const hitTargets = hotspots.map(h => h.hit);

  /* ---------------------------------------------------------------------
     Post-processing: bloom + a screen-space scan line

     Bloom is what makes the hotspots and lit windows read as *glowing*
     rather than merely bright. The scan pass adds the red sweep from the
     reference effect, timed to the world-space scan so the two read as one
     thing. If any of it fails to compile we fall back to a plain render
     rather than showing the visitor a blank canvas.
     --------------------------------------------------------------------- */
  const ScanLineShader = {
    uniforms: {
      tDiffuse:  { value: null },
      uProgress: { value: 0 },
      uStrength: { value: 1 }
    },
    vertexShader: `
      varying vec2 vUv;
      void main() {
        vUv = uv;
        gl_Position = projectionMatrix * modelViewMatrix * vec4( position, 1.0 );
      }`,
    fragmentShader: `
      uniform sampler2D tDiffuse;
      uniform float uProgress;
      uniform float uStrength;
      varying vec2 vUv;
      void main() {
        vec4 c = texture2D( tDiffuse, vUv );
        float d = abs( vUv.y - uProgress );
        float halo = 1.0 - smoothstep( 0.0, 0.055, d );
        float core = 1.0 - smoothstep( 0.0, 0.0035, d );
        vec3 red = vec3( 1.0, 0.18, 0.32 );
        float amount = ( halo * 0.20 + core * 0.85 ) * uStrength;
        c.rgb += red * amount;

        /* This pass runs last, so it owns the alpha that reaches the page.
           The post-processing chain flattens alpha to 1, which would paint a
           black rectangle over the hero's CSS gradient. Rebuilding alpha from
           luminance is reliable here because the scene is bright geometry on
           an empty background: lit pixels become opaque, empty ones stay
           fully transparent, and the gradient shows through as intended. */
        float lum = max( c.r, max( c.g, c.b ) );
        c.a = clamp( smoothstep( 0.035, 0.20, lum ) + amount * 0.9, 0.0, 1.0 );
        gl_FragColor = c;
      }`
  };

  let composer = null;
  let scanPass = null;
  try {
    composer = new EffectComposer(renderer);
    composer.addPass(new RenderPass(scene, camera));
    composer.addPass(new UnrealBloomPass(
      new THREE.Vector2(512, 512),
      0.52,   // strength — enough to bloom the hotspots, not wash the house out
      0.62,   // radius
      0.30    // threshold
    ));
    composer.addPass(new OutputPass());
    // Deliberately after OutputPass: this pass owns the final alpha (see shader)
    scanPass = new ShaderPass(ScanLineShader);
    composer.addPass(scanPass);
  } catch (err) {
    console.warn('[IQ Homes] post-processing unavailable, rendering plain:', err);
    composer = null;
  }

  /* ---------------------------------------------------------------------
     Camera orbit (custom — light and exactly the feel we want)
     --------------------------------------------------------------------- */
  const orbit = {
    theta: 0.82, phi: 1.21, radius: 15.5,
    tTheta: 0.82, tPhi: 1.21, tRadius: 15.5
  };
  const PHI_MIN = 0.66, PHI_MAX = 1.42;

  let dragging = false;
  let pointerId = null;
  let last = { x: 0, y: 0 };
  let moved = 0;
  let idleSince = performance.now();
  let hasInteracted = false;

  function markInteraction() {
    idleSince = performance.now();
    if (!hasInteracted) {
      hasInteracted = true;
      hint && hint.classList.add('is-hidden');
    }
  }

  canvas.addEventListener('pointerdown', e => {
    if (e.pointerType === 'mouse' && e.button !== 0) return;
    dragging = true;
    pointerId = e.pointerId;
    moved = 0;
    last.x = e.clientX;
    last.y = e.clientY;
    canvas.setPointerCapture(e.pointerId);
    canvas.classList.add('is-grabbing');
    markInteraction();
  });

  canvas.addEventListener('pointermove', e => {
    if (dragging && e.pointerId === pointerId) {
      const dx = e.clientX - last.x;
      const dy = e.clientY - last.y;
      moved += Math.abs(dx) + Math.abs(dy);
      orbit.tTheta -= dx * 0.0062;
      orbit.tPhi = Math.min(PHI_MAX, Math.max(PHI_MIN, orbit.tPhi - dy * 0.0038));
      last.x = e.clientX;
      last.y = e.clientY;
      markInteraction();
    } else {
      updateHover(e);
    }
  });

  function endDrag(e) {
    if (!dragging || (pointerId !== null && e.pointerId !== pointerId)) return;
    dragging = false;
    canvas.classList.remove('is-grabbing');
    try { canvas.releasePointerCapture(e.pointerId); } catch (_) {}
    // A tap (not a drag) selects whatever is under the pointer
    if (moved < 8) selectAtPointer(e);
    pointerId = null;
  }
  canvas.addEventListener('pointerup', endDrag);
  canvas.addEventListener('pointercancel', endDrag);
  canvas.addEventListener('pointerleave', () => {
    if (!dragging) clearHover();
  });

  // Keyboard access
  canvas.setAttribute('tabindex', '0');
  canvas.addEventListener('keydown', e => {
    const step = 0.18;
    if (e.key === 'ArrowLeft')  { orbit.tTheta += step; markInteraction(); e.preventDefault(); }
    if (e.key === 'ArrowRight') { orbit.tTheta -= step; markInteraction(); e.preventDefault(); }
    if (e.key === 'ArrowUp')    { orbit.tPhi = Math.max(PHI_MIN, orbit.tPhi - step * 0.6); markInteraction(); e.preventDefault(); }
    if (e.key === 'ArrowDown')  { orbit.tPhi = Math.min(PHI_MAX, orbit.tPhi + step * 0.6); markInteraction(); e.preventDefault(); }
  });

  /* ---------------------------------------------------------------------
     Picking
     --------------------------------------------------------------------- */
  const ray = new THREE.Raycaster();
  const ndc = new THREE.Vector2();
  let hoverIdx = -1;
  let activeIdx = -1;

  function pointerToNDC(e) {
    const r = canvas.getBoundingClientRect();
    ndc.x = ((e.clientX - r.left) / r.width) * 2 - 1;
    ndc.y = -((e.clientY - r.top) / r.height) * 2 + 1;
    return r;
  }

  function pick(e) {
    pointerToNDC(e);
    ray.setFromCamera(ndc, camera);
    const hits = ray.intersectObjects(hitTargets, false);
    return hits.length ? hits[0].object.userData.index : -1;
  }

  function updateHover(e) {
    const idx = pick(e);
    if (idx === hoverIdx) {
      if (idx > -1) positionTip(e);
      return;
    }
    hoverIdx = idx;
    canvas.classList.toggle('is-pointing', idx > -1);
    if (idx > -1) {
      tip.textContent = hotspots[idx].name;
      tip.classList.add('is-visible');
      positionTip(e);
    } else {
      tip.classList.remove('is-visible');
    }
  }

  function positionTip(e) {
    const r = canvas.getBoundingClientRect();
    tip.style.left = (e.clientX - r.left) + 'px';
    tip.style.top = (e.clientY - r.top) + 'px';
  }

  function clearHover() {
    hoverIdx = -1;
    canvas.classList.remove('is-pointing');
    tip.classList.remove('is-visible');
  }

  function selectAtPointer(e) {
    const idx = pick(e);
    if (idx === -1) { closeDetail(); return; }
    openDetail(idx);
  }

  function openDetail(idx) {
    activeIdx = idx;
    hotspots.forEach((h, i) => { h.active = i === idx; });
    const d = hotspots[idx];
    detailTitle.textContent = d.name;
    detailBody.textContent = d.blurb;
    detail.classList.add('is-visible');
    detail.setAttribute('aria-hidden', 'false');
    markInteraction();
  }

  function closeDetail() {
    activeIdx = -1;
    hotspots.forEach(h => { h.active = false; });
    detail.classList.remove('is-visible');
    detail.setAttribute('aria-hidden', 'true');
  }

  detailClose && detailClose.addEventListener('click', closeDetail);

  /* ---------------------------------------------------------------------
     Resize
     --------------------------------------------------------------------- */
  function resize() {
    const w = stageEl.clientWidth;
    const h = stageEl.clientHeight;
    if (!w || !h) return;
    renderer.setSize(w, h, false);
    if (composer) composer.setSize(w, h);
    camera.aspect = w / h;
    // Pull the camera back a little on narrow viewports so the house still fits
    orbit.tRadius = w < 620 ? 19 : w < 900 ? 17.2 : 15.5;
    camera.updateProjectionMatrix();
  }
  const ro = new ResizeObserver(resize);
  ro.observe(stageEl);
  resize();

  /* ---------------------------------------------------------------------
     Render loop
     --------------------------------------------------------------------- */
  let visible = true;
  new IntersectionObserver(entries => {
    visible = entries[0].isIntersecting;
  }, { threshold: 0.01 }).observe(stageEl);

  const clock = new THREE.Clock();
  let firstFrame = true;

  function frame() {
    requestAnimationFrame(frame);
    if (!visible) return;

    const t = clock.getElapsedTime();
    const now = performance.now();

    // Idle auto-rotate
    if (!reduceMotion && !dragging && now - idleSince > 3800) {
      orbit.tTheta += 0.0019;
    }

    // Damping
    orbit.theta  += (orbit.tTheta  - orbit.theta)  * 0.085;
    orbit.phi    += (orbit.tPhi    - orbit.phi)    * 0.085;
    orbit.radius += (orbit.tRadius - orbit.radius) * 0.06;

    const sp = Math.sin(orbit.phi);
    camera.position.set(
      target.x + orbit.radius * sp * Math.sin(orbit.theta),
      target.y + orbit.radius * Math.cos(orbit.phi),
      target.z + orbit.radius * sp * Math.cos(orbit.theta)
    );
    camera.lookAt(target);

    // Hotspot pulse + hover/active emphasis
    hotspots.forEach((h, i) => {
      const on = i === hoverIdx || h.active;
      const pulse = reduceMotion ? 0 : Math.sin(t * 2.1 + h.phase) * 0.5 + 0.5;
      const base = on ? 1.28 : 0.66;
      const s = base + pulse * (on ? 0.2 : 0.14);
      h.sprite.scale.setScalar(s);
      h.sprite.material.opacity = on ? 1 : 0.62 + pulse * 0.2;
      h.core.scale.setScalar(on ? 1.5 : 1);
      if (!reduceMotion) h.group.position.y = h.pos[1] + Math.sin(t * 1.2 + h.phase) * 0.012;
    });

    // Room lights respond to the focused device
    const focusRoom = hoverIdx > -1 ? hotspots[hoverIdx].room
                    : activeIdx > -1 ? hotspots[activeIdx].room
                    : null;
    Object.entries(roomLights).forEach(([name, light]) => {
      const want = light.userData.base * (focusRoom === name ? 3.1 : 1);
      light.intensity += (want - light.intensity) * 0.1;
    });

    // Blinds drift open/closed when the blinds hotspot is focused
    const blindsOn = focusRoom === 'bedroom';
    const wantY = blindsOn ? F2 + 2.05 : F2 + 1.55;
    blind.position.y += (wantY - blind.position.y) * 0.07;

    /* --- The scan sweep -------------------------------------------------
       One value drives both halves of the effect: the dot-matrix band
       climbing the building in world space, and the red line crossing the
       screen. Same easing as the reference component, so it breathes
       up and down rather than snapping back.                             */
    if (reduceMotion) {
      scanUniforms.uScanOn.value = 0;
      if (scanPass) scanPass.uniforms.uStrength.value = 0;
    } else {
      const p = Math.sin(t * 0.42) * 0.5 + 0.5;
      scanUniforms.uScanY.value = -0.6 + p * 7.8;
      scanUniforms.uScanOn.value = 1;
      if (scanPass) {
        scanPass.uniforms.uProgress.value = p;
        // Ease the line off at the extremes so it doesn't sit parked at an edge
        scanPass.uniforms.uStrength.value =
          Math.min(1, Math.sin(p * Math.PI) * 1.9);
      }
    }

    if (composer) composer.render();
    else renderer.render(scene, camera);

    if (firstFrame) {
      firstFrame = false;
      loader && loader.classList.add('is-hidden');
      if (!reduceMotion && !isCoarse) {
        setTimeout(() => hint && !hasInteracted && hint.classList.remove('is-hidden'), 400);
      }
    }
  }
  frame();

  /* Let other scripts drive the scene (e.g. service cards on the page) */
  stageEl.focusDevice = id => {
    const idx = hotspots.findIndex(h => h.id === id);
    if (idx > -1) {
      openDetail(idx);
      // Swing the camera toward the device
      const p = hotspots[idx].group.position;
      orbit.tTheta = Math.atan2(p.x, p.z) + 0.55;
      orbit.tPhi = 1.0;
    }
  };

  return { scene, camera, renderer };
}
