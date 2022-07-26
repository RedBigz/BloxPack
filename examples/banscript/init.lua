local Players = game:GetService("Players")
local bannedPlayers = require("banned_players")

Players.PlayerAdded:Connect(function(player)
	for _, v in pairs(bannedPlayers) do
		if player.UserId == v then
			player:Kick("You have been banned from the game.")
		end
	end
end)