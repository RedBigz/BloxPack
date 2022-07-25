-- Put this script into ReplicatedStorage
-- Make sure it's named "RPack"
-- Must be a ModuleScript

return function (data)
	local scriptExports = {}
	local cscript = "init"
	local ocscript = "init"

	local function Export(value, name)
		if scriptExports[cscript] == nil then
			scriptExports[cscript] = {}
		end
		scriptExports[cscript][name] = value
	end

	local function Import(module, ignoreDefault)
		ocscript = cscript
		cscript = module
		data[module](Import, Export)
		local d = scriptExports[cscript]
		if d.default and not ignoreDefault then
			d = d.default
		end
		cscript = ocscript
		return d
	end

	data.init(Import, Export)
end