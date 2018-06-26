# RenderDoc Python scripts, powered by IronPython 2.7.4.1000
# The 'pyrenderdoc' object is the Core class instance.
# The 'renderdoc' module is available, as the matching namespace in C#
from os import listdir
from os.path import isfile, join
import time

def find_call(drawcalls_, name_, first=True):
	scene_id = -1
	for i, dc in enumerate(drawcalls_):
		if dc.name == name_:
			scene_id = i
			if first:
				break
	return scene_id


path_to_save = 'O:\\unix\\projects\\grail\\krematas\\data\\play_for_data\\'
capture = 9

filenames = [f for f in listdir(join(path_to_save, 'captures', 'capture%d' % capture)) if isfile(join(path_to_save, 'captures', 'capture%d' % capture, f))]
filenames.sort()
start = 0
end = len(filenames)
filenames = filenames[start:end]

config = {}
config['callname_rgb'] = ['pfx::nonz_combine', 'pfx::nonz_combine', 'pfx::nonz_combine']
config['texturename_rgb'] = ['Texture2D RTV 15421', 'Texture2D RTV 84', 'Texture2D RTV 15421']
config['callname_depth'] = ['Rain::Draw', 'MotionBlur::RenderPlayerVelocity', 'MSAA context']
config['texturename_depth'] = ['Texture2D DSV 90', 'Texture2D DSV 90', 'Texture2D DSV 15425']

f_id = 0
f = filenames[f_id]

for f_id, f in enumerate(filenames):

	fname_as_int = f_id+start
	print('%d: %05d' % (f_id, fname_as_int))

	pyrenderdoc.AppWindow.LoadLogfile(join(path_to_save, 'captures', 'capture%d' % capture, f), False, True)

	time.sleep(5)

	#frameId = pyrenderdoc.FrameInfo.frameNumber
	drawcalls = pyrenderdoc.GetDrawcalls()

	capture_id = -1
	capture_type0 = find_call(drawcalls, 'GAME_STATE_IS_GAMESTATE_PLAY')
	if capture_type0 > -1:
		capture_id = 0
	else:
		capture_type1 = find_call(drawcalls, 'GAME_STATE_IS_GAMESTATE_OUTOFPLAY')
		if capture_type1 > -1:
			capture_id = 1

	capture_id = 2
	scene_id = find_call(drawcalls, 'GameSceneManager__RenderScene')

	# ==========================================================================================
	# RGB
	rgb_call = find_call(drawcalls[scene_id].children[0].children, config['callname_rgb'][capture_id])
	my_dc = drawcalls[scene_id].children[0].children[rgb_call]

	eventID = my_dc.children[0].eventID
	pyrenderdoc.SetEventID(None, eventID)
	commonState=pyrenderdoc.CurPipelineState
	print(my_dc.name)
	rgb_tex = None
	for tex in pyrenderdoc.CurTextures:
		# print(tex.name)
		buff = 'Texture2D RTV %s' % commonState.GetOutputTargets()[0].Id
		if tex.name==buff:
			rgb_tex = tex
	print(rgb_tex.name)
	texsave = renderdoc.TextureSave()

	#cnt = pyrenderdoc.FrameInfo.frameNumber

	texsave.sample.mapToArray = False
	texsave.sample.sampleIndex = 0
	texsave.slice.sliceIndex = 0
	texsave.slice.slicesAsGrid = False
	texsave.slice.sliceGridWidth = 1
	texsave.slice.cubeCruciform = False
	texsave.mip = 0

	def saveCallback(r):
		texsave.id = rgb_tex.ID
		texsave.mip = 0
		texsave.slice.sliceIndex = 0
		texsave.comp.blackPoint = 0.0
		texsave.comp.whitePoint = 1.0
		texsave.alpha = renderdoc.AlphaMapping.BlendToCheckerboard
		texsave.destType = renderdoc.FileType.PNG
		r.SaveTexture(texsave,join(path_to_save, 'images', '%05d_%05d.png' % (capture, fname_as_int)))

		print('RGB saved')

	pyrenderdoc.Renderer.Invoke(saveCallback)

	# ==========================================================================================
	# Depth
	depth_call = find_call(drawcalls[scene_id].children[0].children, config['callname_depth'][capture_id])
	my_dc = drawcalls[scene_id].children[0].children[depth_call]
	print(my_dc.name)
	# eventID = my_dc.children[0].eventID
	child_id = find_call(my_dc.children, 'MSAA end', first=False)
	print(child_id)
	eventID = my_dc.children[child_id].eventID
	print(my_dc.children[child_id].name)
	pyrenderdoc.SetEventID(None, eventID)
	commonState=pyrenderdoc.CurPipelineState
	depth_tex = None
	buff = 'Texture2D DSV %s' % commonState.GetDepthTarget().Id
	print(buff)
	for tex in pyrenderdoc.CurTextures:
		
		if tex.name==buff:
			depth_tex = tex
	print(depth_tex.name)
	texsave = renderdoc.TextureSave()

	cnt = pyrenderdoc.FrameInfo.frameNumber

	texsave.sample.mapToArray = False
	texsave.sample.sampleIndex = 0
	texsave.slice.sliceIndex = 0
	texsave.slice.slicesAsGrid = False
	texsave.slice.sliceGridWidth = 1
	texsave.slice.cubeCruciform = False
	texsave.mip = 0

	def saveCallback(r):
		texsave.id = depth_tex.ID
		texsave.mip = -1
		texsave.slice.sliceIndex = -1
		texsave.destType = renderdoc.FileType.DDS
		r.SaveTexture(texsave,join(path_to_save, 'depth', '%05d_%05d.dds' % (capture, fname_as_int)))

		print('Depth saved')

	pyrenderdoc.Renderer.Invoke(saveCallback)
	

#pyrenderdoc.AppWindow.Close()

#aa = dir(depth_tex)
#for i in aa: print i