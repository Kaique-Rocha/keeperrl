// Standalone builds retain keyboard/mouse input without requiring the Steam SDK.
#ifndef USE_STEAMWORKS
#include "steam_input.h"
#include "steam_achievements.h"
#include "achievement_id.h"
void MySteamInput::init() {}
void MySteamInput::detectControllers() {}
void MySteamInput::showBindingScreen() {}
void MySteamInput::showFloatingKeyboard(Rectangle) {}
void MySteamInput::dismissFloatingKeyboard() {}
optional<ControllerKey> MySteamInput::getEvent() { return none; }
void MySteamInput::setGameActionLayer(GameActionLayer layer) { actionLayer = layer; }
pair<double, double> MySteamInput::getJoyPos(ControllerJoy) { return {0, 0}; }
void MySteamInput::runFrame() {}
bool MySteamInput::isPressed(ControllerKey) { return false; }
bool MySteamInput::isRunningOnDeck() { return false; }
optional<FilePath> MySteamInput::getGlyph(ControllerKey) { return none; }
SteamAchievements::SteamAchievements() {}
void SteamAchievements::achieve(AchievementId) {}
#endif
