class Game {
    constructor() {
        this.player = new Player();
        this.monsters = this.createMonsters();
        this.currentMonster = null;
        this.messageElement = document.getElementById("messages");
        this.location = "village";
    }

    createMonsters() {
        return [
            new Monster("Headless Goblin", 30, 50, { name: "Muramasa", damage: 55 }, null),
            new Monster("Succubus", 250, 80, null, { name: "Succubus Stone", effect: "HEALTH_UP" }),
            new Monster("Demon of The Night", 300, 82, { name: "Demon Cleaver", damage: 80 }, null),
            new Monster("Murky Forest Tree Spirit", 350, 100, { name: "Arkhalis", damage: 100 }, { name: "Tree Reinforcement", effect: "DAMAGE_ABSORB" }),
            new Monster("Carmine, the Demon Witch", 600, 200, null, { name: "Demon Idol", effect: "TROPHY" })
        ];
    }

    start() {
        this.appendMessage("Welcome to Nightwood Village!");
        this.appendMessage("Type /start to begin your adventure.");
    }

    appendMessage(message) {
        const newMessage = document.createElement("div");
        newMessage.textContent = message;
        this.messageElement.appendChild(newMessage);
    }

    handleCommand(command) {
        if (command === "/start") {
            this.appendMessage("You meet Lucas the Wonderer...");
            this.appendMessage("Lucas tells you about the monsters in the Murky Forest.");
            this.appendMessage("Use /travel Forest to leave the village and fight the monsters.");
        } else if (command === "/travel Forest") {
            if (this.location === "village") {
                if (!this.currentMonster) {
                    this.location = "forest";
                    this.fightMonster();
                } else {
                    this.appendMessage("You're already fighting a monster. Defeat it before traveling to the forest again.");
                }
            } else {
                this.appendMessage("You are already in the forest.");
            }
        } else if (command === "/village") {
            if (this.location === "forest") {
                this.location = "village";
                this.inBattle = false;
                this.appendMessage("You've returned to the village.");
            } else {
                this.appendMessage("You are already in the village.");
            }
        } else if (command.startsWith("/change weapon ")) {
            const index = parseInt(command.slice(14)) - 1;
            this.player.changeWeapon(index);
            this.player.updatePlayerInfo();
            this.appendMessage("Weapon changed.");
        } else if (command.startsWith("/equip charm ")) {
            const index = parseInt(command.slice(13)) - 1;
            this.player.equipCharm(index);
            this.player.updatePlayerInfo();
            this.appendMessage("Charm equipped.");
        } else {
            this.appendMessage("Unknown command.");
        }
    }

    async fightMonster() {
        this.currentMonster = this.monsters.shift();
        if (!this.currentMonster) {
            this.appendMessage("Congratulations! You've defeated all the monsters!");
            return;
        }
    
        this.appendMessage(`You encounter ${this.currentMonster.name}!`);
        this.inBattle = true;
    
        while (this.player.isAlive() && this.currentMonster.isAlive() && this.inBattle) {
            await new Promise(resolve => {
                const attackHandler = event => {
                    if (event.key === "Enter" && event.target.value.toLowerCase() === "attack") {
                        const playerDamage = this.player.attack(this.currentMonster);
                        this.appendMessage(`You dealt ${playerDamage} damage to ${this.currentMonster.name}.`);
                        
                        const monsterDamage = this.currentMonster.attack(this.player);
                        this.appendMessage(`${this.currentMonster.name} dealt ${monsterDamage} damage to you.`);
                        this.player.updatePlayerInfo();
                        event.target.value = "";
                        inputElement.removeEventListener("keydown", attackHandler);
                        resolve();
                    }
                };
                inputElement.addEventListener("keydown", attackHandler);
            });
        }
    
        if (this.player.isAlive() && this.currentMonster.isAlive()) {
            this.appendMessage("You've returned to the village.");
            this.player.restoreHealth();
            this.player.updatePlayerInfo(); // Update player info after restoring health
        } else if (this.player.isAlive()) {
            this.appendMessage(`You've defeated ${this.currentMonster.name}!`);
            this.player.collectReward(this.currentMonster);
            this.appendMessage("Type /travel Forest to fight the next monster or /village to return to the village.");
            this.currentMonster = null; // Reset the currentMonster
            this.inBattle = false; // Set inBattle to false
        } else {
            this.appendMessage("You Died!");
            this.player.restoreHealth();
            this.appendMessage("You're back in the village, healed and ready to try again.");
            this.location = "village"; 
            this.currentMonster = null; // Add this line to reset the currentMonster
        }
        this.inBattle = false;
    }
}

class Player {
    constructor() {
        this.health = 100;
        this.inventory = {
            weapons: { name: "Sword", damage: 30 },
            charms: [],
        };

    }

    isAlive() {
        return this.health > 0;
    }

    attack(monster) {
        if (this.weapon) {
            monster.takeDamage(this.weapon.damage);
        } else {
            // If for some reason, the player doesn't have a weapon, deal a default damage of 10
            monster.takeDamage(10);
        }
    }    
    takeDamage(damage) {
        if (this.hasCharm("DAMAGE_ABSORB") && Math.random() < 0.3) {
            damage = 0;
        }

        this.health -= damage;
    }

    restoreHealth() {
        this.health = 100;
    }

    collectReward(monster) {
        if (monster.weaponDrop) {
            this.inventory.weapons.push(monster.weaponDrop);
        }
        if (monster.charmsDrop) {
            this.inventory.charms.push(monster.charmsDrop);
            if (monster.charmsDrop.effect === "HEALTH_UP") {
                this.health *= 1.1;
                this.updatePlayerInfo();
            }
        }
    }

    changeWeapon(index) {
        if (index >= 0 && index < this.inventory.weapons.length) {
            this.weapon = this.inventory.weapons[index];
        }
    }

    equipCharm(index) {
        if (index >= 0 && index < this.inventory.charms.length) {
            this.charms.push(this.inventory.charms[index]);
            this.inventory.charms.splice(index, 1);
        }
    }

    hasCharm(effect) {
        if (this.charms) {
            return this.charms.some(charm => charm.effect === effect);
        }
        return false;
    }
    updatePlayerInfo() {
        const healthElement = document.getElementById("health");
        const weaponElement = document.getElementById("weapon");
        const charmsElement = document.getElementById("charms");
    
        healthElement.textContent = `Health: ${game.player.health}`;
        weaponElement.textContent = `Weapon: ${game.player.weapon ? game.player.weapon.name : "None"} (Damage: ${game.player.weapon ? game.player.weapon.damage : 0})`;
    
        if (game.player.charms.length > 0) {
            const charmNames = game.player.charms.map(charm => charm.name).join(", ");
            charmsElement.textContent = `Charms: ${charmNames}`;
        } else {
            charmsElement.textContent = "Charms: None";
        }
    
        const inventoryElement = document.getElementById("inventory");
        const weapons = game.player.inventory.weapons.map((weapon, index) => `${index + 1}. ${weapon.name} (Damage: ${weapon.damage})`).join("<br>");
        const charms = game.player.inventory.charms.map((charm, index) => `${index + 1}. ${charm.name}`).join("<br>");
    
        inventoryElement.innerHTML = `
            <h4>Inventory</h4>
            <p>Weapons:</p>
            ${weapons ? weapons : "None"}
            <p>Charms:</p>
            ${charms ? charms : "None"}
        `;
    }


}

class Monster {
    constructor(name, health, attackDamage, weaponDrop, charmsDrop) {
        this.name = name;
        this.health = health;
        this.attackDamage = attackDamage;
        this.weaponDrop = weaponDrop;
        this.charmsDrop = charmsDrop;
    }

    isAlive() {
        return this.health > 0;
    }
    
    attack(player) {
        player.takeDamage(this.attackDamage);
        return this.attackDamage;
    }
    
    takeDamage(damage) {
        this.health -= damage;
    }
}

const inputElement = document.getElementById("input");
const saveButton = document.getElementById("save");
const loadButton = document.getElementById("load");

const game = new Game();
game.start();

inputElement.addEventListener("keydown", async (event) => {
    if (event.key === "Enter") {
        if (game.inBattle) {
            game.appendMessage("Type 'attack' to attack the monster.");
        } else {
            game.handleCommand(event.target.value);
            event.target.value = "";
        }
    }
});

saveButton.addEventListener("click", () => {
localStorage.setItem("game", JSON.stringify(game));
});

loadButton.addEventListener("click", () => {
const savedGame = JSON.parse(localStorage.getItem("game"));
    if (savedGame) {
        Object.assign(game.player, savedGame.player);
        game.monsters = savedGame.monsters.map(monsterData => new Monster(...Object.values(monsterData)));
    }
});