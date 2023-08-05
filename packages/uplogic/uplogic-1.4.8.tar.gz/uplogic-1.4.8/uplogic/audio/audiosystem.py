'''TODO: Documentation
'''

from bge import logic
from mathutils import Vector
from uplogic.data.globaldb import GlobalDB
import aud
import bpy


DISTANCE_MODELS = {
    'EXPONENT': aud.DISTANCE_MODEL_EXPONENT,
    'EXPONENT_CLAMPED': aud.DISTANCE_MODEL_EXPONENT_CLAMPED,
    'INVERSE': aud.DISTANCE_MODEL_INVERSE,
    'INVERSE_CLAMPED': aud.DISTANCE_MODEL_INVERSE_CLAMPED,
    'LINEAR': aud.DISTANCE_MODEL_LINEAR,
    'LINEAR_CLAMPED': aud.DISTANCE_MODEL_LINEAR_CLAMPED,
    'NONE': aud.DISTANCE_MODEL_INVALID
}


def set_master_volume(volume, aud_system='default') -> None:
    aud_system = GlobalDB.retrieve('uplogic.audio').get(aud_system)
    if aud_system:
        aud_system.volume = volume


class ULAudioSystem(object):
    '''TODO: Documentation
    '''
    def __init__(self, name: str):
        self.active_sounds = []
        self.name = name
        self.bounces = 0
        self.volume = 1.0
        self.device = aud.Device()
        self.device.distance_model = aud.DISTANCE_MODEL_INVERSE_CLAMPED
        self.device.speed_of_sound = bpy.context.scene.audio_doppler_speed
        self.device.doppler_factor = bpy.context.scene.audio_doppler_factor
        self.reverb_volumes = []
        self.scene = logic.getCurrentScene()
        self.listener = self.scene.active_camera
        self.old_lis_pos = self.listener.worldPosition.copy()
        self.setup(self.scene)
    
    def setup(self, scene=None):
        if scene is None:
            self.scene = logic.getCurrentScene()
        else:
            self.scene = scene
        for obj in self.scene.objects:
            if getattr(obj.blenderObject, 'reverb_volume', False) and not obj.blenderObject.data:
                self.reverb_volumes.append(obj)
        self.reverb = len(self.reverb_volumes) > 0
        GlobalDB.retrieve('uplogic.audio').put(self.name, self)
        bpy.app.handlers.game_post.append(self.shutdown)
        self.scene.post_draw.append(self.update)

    def get_distance_model(self, name):
        return DISTANCE_MODELS.get(name, aud.DISTANCE_MODEL_INVERSE_CLAMPED)

    def compute_listener_velocity(self, listener):
        wpos = listener.worldPosition.copy()
        olp = self.old_lis_pos
        vel = (
            (wpos.x - olp.x) * 50,
            (wpos.y - olp.y) * 50,
            (wpos.z - olp.z) * 50
        )
        self.old_lis_pos = wpos
        return vel

    def update(self):
        scene = logic.getCurrentScene()
        if scene is not self.scene:
            self.setup(scene)
        cam = scene.active_camera
        self.reverb = False
        self.listener = cam
        if not self.active_sounds:
            return  # do not update if no sound has been installed
        # update the listener data
        cpos = cam.worldPosition
        distances = {}
        if self.reverb_volumes:
            for obj in self.reverb_volumes:
                dist = obj.getDistanceTo(cam)
                if dist > 50:
                    continue
                else:
                    distances[dist] = obj
            min_dist = distances[min(distances.keys())]
            obj = min_dist
            ob = obj.blenderObject
            r = ob.empty_display_size
            wpos = obj.worldPosition
            sca = ob.scale
            # if cam.getDistanceTo(obj) < ob.empty_display_size:
            in_range = (
                wpos.x - r*sca.x < cpos.x < wpos.x + r*sca.x and
                wpos.y - r*sca.y < cpos.y < wpos.y + r*sca.y and
                wpos.z - r*sca.z < cpos.z < wpos.z + r*sca.z
            )
            if in_range:
                self.reverb = True
                self.bounces = ob.reverb_samples
        listener_vel = self.compute_listener_velocity(cam)
        dev = self.device
        dev.listener_location = cpos
        dev.listener_orientation = cam.worldOrientation.to_quaternion()
        dev.listener_velocity = listener_vel
        for s in self.active_sounds:
            s.update()

    def add(self, sound):
        self.active_sounds.append(sound)

    def remove(self, sound):
        self.active_sounds.remove(sound)

    def shutdown(self, a, b):
        self.device.stopAll()
        bpy.app.handlers.game_post.remove(self.shutdown)
